import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.rbac import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
)
from app.schemas.rbac import PermissionRead
from app.services.rbac_service import RbacService
from app.services.role_permission_service import RolePermissionService


router = APIRouter(
    prefix="/establishments",
    tags=["role-permissions"],
)


def get_role_permission_service(
    session: AsyncSession = Depends(get_db),
) -> RolePermissionService:
    return RolePermissionService(
        role_repo=RoleRepository(session),
        permission_repo=PermissionRepository(session),
        role_permission_repo=RolePermissionRepository(session),
    )


@router.get(
    "/{establishment_id}/roles/{role_id}/permissions",
    response_model=list[PermissionRead],
)
async def list_role_permissions(
    establishment_id: uuid.UUID,
    role_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: RolePermissionService = Depends(
        get_role_permission_service
    ),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.manage",
        establishment_id=establishment_id,
    )

    return await service.list_permissions(
        establishment_id=establishment_id,
        role_id=role_id,
    )


@router.post(
    "/{establishment_id}/roles/{role_id}/permissions/{permission_id}",
    status_code=status.HTTP_201_CREATED,
)
async def assign_permission(
    establishment_id: uuid.UUID,
    role_id: uuid.UUID,
    permission_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: RolePermissionService = Depends(
        get_role_permission_service
    ),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.manage",
        establishment_id=establishment_id,
    )

    return await service.assign_permission(
        establishment_id=establishment_id,
        role_id=role_id,
        permission_id=permission_id,
    )


@router.delete(
    "/{establishment_id}/roles/{role_id}/permissions/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_permission(
    establishment_id: uuid.UUID,
    role_id: uuid.UUID,
    permission_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: RolePermissionService = Depends(
        get_role_permission_service
    ),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.manage",
        establishment_id=establishment_id,
    )

    await service.remove_permission(
        establishment_id=establishment_id,
        role_id=role_id,
        permission_id=permission_id,
    )