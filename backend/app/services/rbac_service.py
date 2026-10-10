import uuid

from sqlalchemy import select

from app.core.exceptions import ConflictException, ForbiddenException, NotFoundException, UnauthorizedException
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models import Role
from app.models.organization import Establishment
from app.models.rbac import UserEstablishment, UserRole
from app.repositories.rbac import (
    PermissionRepository, RolePermissionRepository, RoleRepository, UserRepository, UserRoleRepository,
)
from app.schemas.rbac import RoleCreate, UserCreate, UserRead, ScopeType, EstablishmentBrief
from app.services.invitation_service import InvitationService


class RbacService:
    def __init__(
            self,
            user_repo: UserRepository,
            role_repo: RoleRepository,
            permission_repo: PermissionRepository,
            role_permission_repo: RolePermissionRepository,
            user_role_repo: UserRoleRepository,
            invitation_service: InvitationService,
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.permission_repo = permission_repo
        self.role_permission_repo = role_permission_repo
        self.user_role_repo = user_role_repo
        self.invitation_service = invitation_service

    # --- Auth ---

    async def register_user(self, data: UserCreate):
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise ConflictException("Cet email est déjà utilisé")

        payload = data.model_dump(exclude={"password"})
        payload["password_hash"] = hash_password(data.password)
        return await self.user_repo.create(payload)

    async def authenticate(self, email: str, password: str) -> dict:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedException("Email ou mot de passe incorrect")
        if user.status != "active":
            raise ForbiddenException("Compte désactivé")

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    async def get_current_user(self, user_id: uuid.UUID):
        user = await self.user_repo.get(user_id)
        if not user:
            raise UnauthorizedException("Utilisateur introuvable")

        permissions = await self.user_role_repo.get_permission_codes_for_user(
            user_id
        )

        establishment_id = await self._get_user_establishment_id(user_id)
        scope = await self._get_user_scope(user_id)

        user_data = UserRead.model_validate(user).model_dump()
        user_data["permissions"] = permissions
        user_data["establishment_id"] = establishment_id
        user_data["scope"] = scope
        user_data["establishments"] = await self._get_user_establishments(
            user_id, scope
        )

        return user_data

    async def _get_user_scope(
        self,
        user_id: uuid.UUID,
    ) -> ScopeType:
        # Hiérarchie : PLATFORM > ORGANIZATION > ESTABLISHMENT.
        # On retourne le scope le plus haut trouvé.
        for scope in (ScopeType.PLATFORM, ScopeType.ORGANIZATION, ScopeType.ESTABLISHMENT):
            stmt = (
                select(UserRole.role_id)
                .join(Role, Role.id == UserRole.role_id)
                .where(
                    UserRole.user_id == user_id,
                    Role.scope_type == scope,
                    UserRole.deleted_at.is_(None),
                )
                .limit(1)
            )

            result = await self.user_repo.session.execute(stmt)

            if result.scalar_one_or_none() is not None:
                return scope

        return ScopeType.ESTABLISHMENT

    async def _get_user_establishment_id(
        self,
        user_id: uuid.UUID,
    ) -> uuid.UUID | None:
        stmt = (
            select(UserEstablishment.establishment_id)
            .where(
                UserEstablishment.user_id == user_id,
                UserEstablishment.deleted_at.is_(None),
            )
            .limit(1)
        )

        result = await self.user_repo.session.execute(stmt)

        return result.scalar_one_or_none()

    async def _get_user_establishments(
        self,
        user_id: uuid.UUID,
        scope: ScopeType,
    ) -> list[EstablishmentBrief]:
        if scope == ScopeType.PLATFORM:
            # Le Super Admin voit tous les établissements de la plateforme
            stmt = (
                select(Establishment.id, Establishment.name)
                .where(Establishment.deleted_at.is_(None))
                .order_by(Establishment.name)
            )
            result = await self.user_repo.session.execute(stmt)
            return [
                EstablishmentBrief(id=row.id, name=row.name)
                for row in result.all()
            ]

        # Pour les autres rôles (ESTABLISHMENT / ORGANIZATION), on combine
        # deux sources d'établissements accessibles :
        #  1. les liaisons explicites via user_establishments ;
        #  2. les établissements portés par un UserRole (UserRole.establishment_id).
        by_user_est = select(Establishment.id, Establishment.name).join(
            UserEstablishment,
            UserEstablishment.establishment_id == Establishment.id,
        ).where(
            UserEstablishment.user_id == user_id,
            UserEstablishment.deleted_at.is_(None),
            Establishment.deleted_at.is_(None),
        )

        by_role = select(Establishment.id, Establishment.name).join(
            UserRole,
            UserRole.establishment_id == Establishment.id,
        ).where(
            UserRole.user_id == user_id,
            UserRole.establishment_id.is_not(None),
            UserRole.deleted_at.is_(None),
            Establishment.deleted_at.is_(None),
        )

        combined = by_user_est.union(by_role).order_by(Establishment.name)

        result = await self.user_repo.session.execute(combined)

        return [
            EstablishmentBrief(id=row.id, name=row.name)
            for row in result.all()
        ]

    # --- RBAC ---

    async def create_role(self, data: RoleCreate):
        return await self.role_repo.create(data.model_dump())

    async def assign_permission(self, role_id: uuid.UUID, permission_id: uuid.UUID):
        role = await self.role_repo.get(role_id)
        if not role:
            raise NotFoundException("Rôle introuvable")
        permission = await self.permission_repo.get(permission_id)
        if not permission:
            raise NotFoundException("Permission introuvable")
        return await self.role_permission_repo.create(
            {"role_id": role_id, "permission_id": permission_id}
        )

    async def assign_role_to_user(
        self,
        user_id: uuid.UUID,
        role_id: uuid.UUID,
        organization_id: uuid.UUID | None = None,
        establishment_id: uuid.UUID | None = None,
    ):
        user = await self.user_repo.get(user_id)
        if not user:
            raise NotFoundException("Utilisateur introuvable")
        role = await self.role_repo.get(role_id)
        if not role:
            raise NotFoundException("Rôle introuvable")
        return await self.user_role_repo.create({
            "user_id": user_id,
            "role_id": role_id,
            "organization_id": organization_id,
            "establishment_id": establishment_id,
        })

    async def check_permission(
            self,
            user_id: uuid.UUID,
            permission_code: str,
            organization_id: uuid.UUID | None = None,
            establishment_id: uuid.UUID | None = None,
    ) -> bool:
        return await self.user_role_repo.has_permission(
            user_id, permission_code, organization_id=organization_id, establishment_id=establishment_id
        )

    async def require_permission(
            self,
            user_id: uuid.UUID,
            permission_code: str,
            organization_id: uuid.UUID | None = None,
            establishment_id: uuid.UUID | None = None,
    ) -> None:
        allowed = await self.check_permission(
            user_id=user_id,
            permission_code=permission_code,
            organization_id=organization_id,
            establishment_id=establishment_id,
        )

        if not allowed:
            raise ForbiddenException(
                f"Permission requise : {permission_code}"
            )

    async def assign_default_establishment_admin_permissions(
            self,
            role_id: uuid.UUID,
    ):
        role = await self.role_repo.get(role_id)

        if not role:
            raise NotFoundException("Rôle introuvable")

        permissions = await self.permission_repo.list(limit=1000)

        existing_permissions = await self.role_permission_repo.get_permissions_for_role(
            role_id
        )

        existing_permission_ids = {
            permission.id
            for permission in existing_permissions
        }

        excluded_codes = {
            "onboarding.review",
            "organization.create",
            "organization.read",
            "organization.update",
            "organization.delete",
            "subscription.create",
            "subscription.read",
            "subscription.update",
            "subscription.delete",
        }

        assigned_permissions = []

        for permission in permissions:
            if permission.code in excluded_codes:
                continue

            if permission.id in existing_permission_ids:
                continue

            role_permission = await self.role_permission_repo.create(
                {
                    "role_id": role_id,
                    "permission_id": permission.id,
                }
            )

            assigned_permissions.append(role_permission)

        return assigned_permissions

    async def accept_invitation(
            self,
            token: str,
            password: str,
    ):
        invitation = await self.invitation_service.get_valid_invitation(
            token
        )

        user = await self.user_repo.get(invitation.user_id)

        if not user:
            raise NotFoundException(
                "Utilisateur associé à cette invitation introuvable"
            )

        user.password_hash = hash_password(password)
        user.status = "active"

        await self.invitation_service.consume_invitation(
            invitation
        )

        await self.user_repo.session.flush()
        await self.user_repo.session.refresh(user)

        return user

    async def sync_establishment_admin_permissions(self, role_id: uuid.UUID):
        role = await self.role_repo.get(role_id)

        if not role:
            raise NotFoundException("Rôle introuvable")

        if not role.is_system:
            raise ConflictException(
                "Ce rôle n'est pas un rôle système d'établissement"
            )

        if role.scope_type.value != "ESTABLISHMENT":
            raise ConflictException(
                "Le rôle doit être de portée établissement"
            )

        permissions = await self.permission_repo.list_all()

        excluded_codes = {
            "onboarding.review",
            "organization.create",
            "organization.read",
            "organization.update",
            "organization.delete",
            "subscription.create",
            "subscription.read",
            "subscription.update",
            "subscription.delete",
        }

        existing_permissions = await self.role_permission_repo.get_permissions_for_role(
            role.id
        )

        existing_ids = {
            permission.id
            for permission in existing_permissions
        }

        added = 0

        for permission in permissions:
            if permission.code in excluded_codes:
                continue

            if permission.id in existing_ids:
                continue

            await self.role_permission_repo.create({
                "role_id": role.id,
                "permission_id": permission.id,
            })

            added += 1

        return {
            "role_id": role.id,
            "permissions_added": added,
        }



    async def sync_all_establishment_admin_permissions(self):
        roles = await self.role_repo.get_system_establishment_roles()

        permissions = await self.permission_repo.list_all()

        excluded_codes = {
            "onboarding.review",
            "organization.create",
            "organization.read",
            "organization.update",
            "organization.delete",
            "subscription.create",
            "subscription.read",
            "subscription.update",
            "subscription.delete",
        }

        synced_roles = 0
        added_permissions = 0

        for role in roles:
            # Garde de robustesse : on ne cible que les rôles système
            # d'établissement (is_system), indépendamment du nom.
            if not role.is_system:
                continue

            existing_permissions = (
                await self.role_permission_repo.get_permissions_for_role(role.id)
            )

            existing_ids = {
                permission.id
                for permission in existing_permissions
            }

            role_added = 0

            for permission in permissions:
                if permission.code in excluded_codes:
                    continue

                if permission.id in existing_ids:
                    continue

                await self.role_permission_repo.create({
                    "role_id": role.id,
                    "permission_id": permission.id,
                })

                role_added += 1

            if role_added > 0:
                synced_roles += 1
                added_permissions += role_added

        return {
            "roles_synced": synced_roles,
            "permissions_added": added_permissions,
        }
