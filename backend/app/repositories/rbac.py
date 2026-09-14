import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.rbac import Permission, Role, RolePermission, User, UserRole
from app.repositories.base import BaseRepository
from app.schemas.rbac import ScopeType


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email, User.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class RoleRepository(BaseRepository[Role]):
    model = Role

    async def get_by_scope(
        self,
        scope_type: str,
        organization_id: uuid.UUID | None = None,
        establishment_id: uuid.UUID | None = None,
    ) -> list[Role]:
        stmt = select(Role).where(Role.scope_type == scope_type, Role.deleted_at.is_(None))
        if organization_id:
            stmt = stmt.where(Role.organization_id == organization_id)
        if establishment_id:
            stmt = stmt.where(Role.establishment_id == establishment_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_system_establishment_roles(self):
        stmt = select(Role).where(
            Role.scope_type == ScopeType.ESTABLISHMENT,
            Role.is_system.is_(True),
            Role.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()

class PermissionRepository(BaseRepository[Permission]):
    model = Permission

    async def get_by_code(self, code: str) -> Permission | None:
        stmt = select(Permission).where(Permission.code == code)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self):
        stmt = select(Permission).where(
            Permission.deleted_at.is_(None)
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()


class RolePermissionRepository(BaseRepository[RolePermission]):
    model = RolePermission

    async def get_permissions_for_role(
        self,
        role_id: uuid.UUID,
    ) -> list[Permission]:
        stmt = (
            select(Permission)
            .join(
                RolePermission,
                RolePermission.permission_id == Permission.id,
            )
            .where(
                RolePermission.role_id == role_id,
                RolePermission.deleted_at.is_(None),
            )
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_role_permission(
        self,
        role_id: uuid.UUID,
        permission_id: uuid.UUID,
    ) -> RolePermission | None:
        stmt = select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
            RolePermission.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def remove_permission(
        self,
        role_permission: RolePermission,
    ) -> RolePermission:
        return await self.soft_delete(role_permission)


class UserRoleRepository(BaseRepository[UserRole]):
    model = UserRole

    async def get_roles_for_user(
        self, user_id: uuid.UUID, establishment_id: uuid.UUID | None = None
    ) -> list[UserRole]:
        stmt = (
            select(UserRole)
            .options(selectinload(UserRole.role))
            .where(UserRole.user_id == user_id, UserRole.deleted_at.is_(None))
        )
        if establishment_id:
            stmt = stmt.where(UserRole.establishment_id == establishment_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def has_permission(
            self,
            user_id: uuid.UUID,
            permission_code: str,
            organization_id: uuid.UUID | None = None,
            establishment_id: uuid.UUID | None = None,
    ) -> bool:
        stmt = (
            select(UserRole)
            .join(Role, Role.id == UserRole.role_id)
            .join(RolePermission, RolePermission.role_id == Role.id)
            .join(Permission, Permission.id == RolePermission.permission_id)
            .where(UserRole.user_id == user_id, Permission.code == permission_code)
        )

        # PLATFORM : aucun scope à vérifier, la permission s'applique partout
        # ORGANIZATION : le user_role doit correspondre à l'organization_id demandé
        # ESTABLISHMENT : le user_role doit correspondre à l'establishment_id demandé
        conditions = [Role.scope_type == "PLATFORM"]

        if organization_id is not None:
            conditions.append(
                (Role.scope_type == "ORGANIZATION") & (UserRole.organization_id == organization_id)
            )
        if establishment_id is not None:
            conditions.append(
                (Role.scope_type == "ESTABLISHMENT") & (UserRole.establishment_id == establishment_id)
            )

        from sqlalchemy import or_
        stmt = stmt.where(or_(*conditions))

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_user_role(
            self,
            user_id: uuid.UUID,
            role_id: uuid.UUID,
            establishment_id: uuid.UUID,
    ) -> UserRole | None:
        stmt = select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id,
            UserRole.establishment_id == establishment_id,
            UserRole.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def remove_role(
            self,
            user_role: UserRole,
    ) -> UserRole:
        return await self.soft_delete(user_role)