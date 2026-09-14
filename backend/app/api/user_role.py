import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.rbac import (
    RoleRepository,
    UserRepository,
    UserRoleRepository,
)
from app.services.rbac_service import RbacService
from app.services.user_role_service import UserRoleService


router = APIRouter(
    prefix="/establishments",
    tags=["user-roles"],
)


def get_user_role_service(
    session: AsyncSession = Depends(get_db),
) -> UserRoleService:
    return UserRoleService(
        user_repo=UserRepository(session),
        role_repo=RoleRepository(session),
        user_role_repo=UserRoleRepository(session),
    )


@router.post(
    "/{establishment_id}/users/{user_id}/roles/{role_id}",
    status_code=status.HTTP_201_CREATED,
)
async def assign_role(
    establishment_id: uuid.UUID,
    user_id: uuid.UUID,
    role_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: UserRoleService = Depends(get_user_role_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.assign",
        establishment_id=establishment_id,
    )

    return await service.assign_role(
        establishment_id=establishment_id,
        user_id=user_id,
        role_id=role_id,
    )


@router.get(
    "/{establishment_id}/users/{user_id}/roles",
)
async def list_user_roles(
    establishment_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: UserRoleService = Depends(get_user_role_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.assign",
        establishment_id=establishment_id,
    )

    return await service.list_roles(
        establishment_id=establishment_id,
        user_id=user_id,
    )


@router.delete(
    "/{establishment_id}/users/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_user_role(
    establishment_id: uuid.UUID,
    user_id: uuid.UUID,
    role_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: UserRoleService = Depends(get_user_role_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.assign",
        establishment_id=establishment_id,
    )

    await service.remove_role(
        establishment_id=establishment_id,
        user_id=user_id,
        role_id=role_id,
    )