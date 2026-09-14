import uuid
from select import select

from app.core.exceptions import ConflictException, NotFoundException
from app.models.rbac import ScopeType, UserEstablishment
from app.repositories.rbac import (
    RoleRepository,
    UserRepository,
    UserRoleRepository,
)


class UserRoleService:
    def __init__(
        self,
        user_repo: UserRepository,
        role_repo: RoleRepository,
        user_role_repo: UserRoleRepository,
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.user_role_repo = user_role_repo

    async def assign_role(
        self,
        establishment_id: uuid.UUID,
        user_id: uuid.UUID,
        role_id: uuid.UUID,
    ):
        user = await self.user_repo.get(user_id)

        if not user:
            raise NotFoundException("Utilisateur introuvable")

        role = await self.role_repo.get(role_id)

        if not role:
            raise NotFoundException("Rôle introuvable")

        if role.scope_type != ScopeType.ESTABLISHMENT:
            raise ConflictException(
                "Seuls les rôles d'établissement peuvent être assignés ici"
            )

        if role.establishment_id != establishment_id:
            raise ConflictException(
                "Ce rôle n'appartient pas à cet établissement"
            )

        stmt = select(UserEstablishment).where(
            UserEstablishment.user_id == user_id,
            UserEstablishment.establishment_id == establishment_id,
        )

        result = await self.user_repo.session.execute(stmt)
        user_establishment = result.scalar_one_or_none()

        if not user_establishment:
            raise ConflictException(
                "Cet utilisateur n'appartient pas à cet établissement"
            )

        existing = await self.user_role_repo.get_user_role(
            user_id=user_id,
            role_id=role_id,
            establishment_id=establishment_id,
        )

        if existing:
            raise ConflictException(
                "Ce rôle est déjà attribué à cet utilisateur"
            )

        return await self.user_role_repo.create(
            {
                "user_id": user_id,
                "role_id": role_id,
                "establishment_id": establishment_id,
            }
        )

    async def list_roles(
        self,
        establishment_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        user = await self.user_repo.get(user_id)

        if not user:
            raise NotFoundException("Utilisateur introuvable")

        stmt = select(UserEstablishment).where(
            UserEstablishment.user_id == user_id,
            UserEstablishment.establishment_id == establishment_id,
        )

        result = await self.user_repo.session.execute(stmt)

        if not result.scalar_one_or_none():
            raise ConflictException(
                "Cet utilisateur n'appartient pas à cet établissement"
            )

        return await self.user_role_repo.get_roles_for_user(
            user_id=user_id,
            establishment_id=establishment_id,
        )

    async def remove_role(
        self,
        establishment_id: uuid.UUID,
        user_id: uuid.UUID,
        role_id: uuid.UUID,
    ):
        user = await self.user_repo.get(user_id)

        if not user:
            raise NotFoundException("Utilisateur introuvable")

        role = await self.role_repo.get(role_id)

        if not role:
            raise NotFoundException("Rôle introuvable")

        if role.establishment_id != establishment_id:
            raise ConflictException(
                "Ce rôle n'appartient pas à cet établissement"
            )

        user_role = await self.user_role_repo.get_user_role(
            user_id=user_id,
            role_id=role_id,
            establishment_id=establishment_id,
        )

        if not user_role:
            raise NotFoundException(
                "Ce rôle n'est pas attribué à cet utilisateur"
            )

        return await self.user_role_repo.remove_role(user_role)