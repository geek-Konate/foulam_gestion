import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.models.rbac import ScopeType
from app.repositories.rbac import RoleRepository
from app.schemas.rbac import RoleCreate, RoleUpdate


class RoleService:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    async def create_role(
        self,
        establishment_id: uuid.UUID,
        data: RoleCreate,
    ):
        # Un rôle d'établissement doit appartenir
        # à l'établissement depuis lequel il est créé.
        if data.scope_type == ScopeType.ESTABLISHMENT:
            if data.establishment_id != establishment_id:
                raise ConflictException(
                    "Le rôle doit appartenir à l'établissement concerné"
                )

        # Un rôle d'organisation ne doit pas recevoir
        # un establishment_id.
        if data.scope_type == ScopeType.ORGANIZATION:
            if data.establishment_id is not None:
                raise ConflictException(
                    "Un rôle d'organisation ne peut pas avoir d'établissement"
                )

            if data.organization_id is None:
                raise ConflictException(
                    "Un rôle d'organisation doit avoir une organisation"
                )

        # Un rôle PLATFORM ne doit appartenir
        # ni à une organisation ni à un établissement.
        if data.scope_type == ScopeType.PLATFORM:
            if (
                data.organization_id is not None
                or data.establishment_id is not None
            ):
                raise ConflictException(
                    "Un rôle PLATFORM ne peut pas être lié à une organisation "
                    "ou un établissement"
                )

        # Pour un rôle d'établissement, on récupère les rôles
        # existants dans cet établissement afin d'éviter
        # les doublons de nom.
        existing_roles = await self.role_repo.get_by_scope(
            scope_type=data.scope_type,
            organization_id=data.organization_id,
            establishment_id=data.establishment_id,
        )

        for role in existing_roles:
            if role.name.lower() == data.name.lower():
                raise ConflictException(
                    "Un rôle portant ce nom existe déjà dans ce périmètre"
                )

        return await self.role_repo.create(
            {
                "name": data.name,
                "description": data.description,
                "scope_type": data.scope_type,
                "organization_id": data.organization_id,
                "establishment_id": data.establishment_id,
                "is_system": False,
            }
        )

    async def list_roles(
        self,
        establishment_id: uuid.UUID,
    ):
        return await self.role_repo.get_by_scope(
            scope_type=ScopeType.ESTABLISHMENT,
            establishment_id=establishment_id,
        )

    async def get_role(
        self,
        establishment_id: uuid.UUID,
        role_id: uuid.UUID,
    ):
        role = await self.role_repo.get(role_id)

        if not role:
            raise NotFoundException("Rôle introuvable")

        if role.scope_type != ScopeType.ESTABLISHMENT:
            raise ConflictException(
                "Ce rôle n'appartient pas à cet établissement"
            )

        if role.establishment_id != establishment_id:
            raise ConflictException(
                "Ce rôle n'appartient pas à cet établissement"
            )

        return role

    async def update_role(
        self,
        establishment_id: uuid.UUID,
        role_id: uuid.UUID,
        data: RoleUpdate,
    ):
        role = await self.get_role(
            establishment_id=establishment_id,
            role_id=role_id,
        )

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing_roles = await self.role_repo.get_by_scope(
                scope_type=ScopeType.ESTABLISHMENT,
                establishment_id=establishment_id,
            )

            for existing_role in existing_roles:
                if (
                    existing_role.id != role.id
                    and existing_role.name.lower()
                    == update_data["name"].lower()
                ):
                    raise ConflictException(
                        "Un rôle portant ce nom existe déjà dans cet établissement"
                    )

        return await self.role_repo.update(
            role,
            update_data,
        )

    async def delete_role(
            self,
            establishment_id: uuid.UUID,
            role_id: uuid.UUID,
    ):
        role = await self.get_role(
            establishment_id=establishment_id,
            role_id=role_id,
        )

        if role.is_system:
            raise ConflictException(
                "Ce rôle système ne peut pas être supprimé"
            )

        return await self.role_repo.soft_delete(role)