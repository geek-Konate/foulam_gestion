import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.rbac import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
)


class RolePermissionService:
    def __init__(
        self,
        role_repo: RoleRepository,
        permission_repo: PermissionRepository,
        role_permission_repo: RolePermissionRepository,
    ):
        self.role_repo = role_repo
        self.permission_repo = permission_repo
        self.role_permission_repo = role_permission_repo

    async def _get_role(
        self,
        establishment_id: uuid.UUID,
        role_id: uuid.UUID,
    ):
        role = await self.role_repo.get(role_id)

        if not role:
            raise NotFoundException("Rôle introuvable")

        if role.scope_type.value != "ESTABLISHMENT":
            raise ConflictException(
                "Ce rôle n'appartient pas à un établissement"
            )

        if role.establishment_id != establishment_id:
            raise ConflictException(
                "Ce rôle n'appartient pas à cet établissement"
            )

        return role

    async def list_permissions(
        self,
        establishment_id: uuid.UUID,
        role_id: uuid.UUID,
    ):
        await self._get_role(
            establishment_id=establishment_id,
            role_id=role_id,
        )

        return await self.role_permission_repo.get_permissions_for_role(
            role_id
        )

    async def assign_permission(
        self,
        establishment_id: uuid.UUID,
        role_id: uuid.UUID,
        permission_id: uuid.UUID,
    ):
        role = await self._get_role(
            establishment_id=establishment_id,
            role_id=role_id,
        )

        permission = await self.permission_repo.get(permission_id)

        if not permission:
            raise NotFoundException("Permission introuvable")

        existing = await self.role_permission_repo.get_role_permission(
            role_id=role.id,
            permission_id=permission.id,
        )

        if existing:
            raise ConflictException(
                "Cette permission est déjà attribuée à ce rôle"
            )

        return await self.role_permission_repo.create(
            {
                "role_id": role.id,
                "permission_id": permission.id,
            }
        )

    async def remove_permission(
        self,
        establishment_id: uuid.UUID,
        role_id: uuid.UUID,
        permission_id: uuid.UUID,
    ):
        role = await self._get_role(
            establishment_id=establishment_id,
            role_id=role_id,
        )

        permission = await self.permission_repo.get(permission_id)

        if not permission:
            raise NotFoundException("Permission introuvable")

        role_permission = (
            await self.role_permission_repo.get_role_permission(
                role_id=role.id,
                permission_id=permission.id,
            )
        )

        if not role_permission:
            raise NotFoundException(
                "Cette permission n'est pas attribuée à ce rôle"
            )

        return await self.role_permission_repo.remove_permission(
            role_permission
        )