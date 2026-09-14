import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.rbac import RoleRepository
from app.schemas.rbac import RoleCreate, RoleRead, RoleUpdate
from app.services.rbac_service import RbacService
from app.services.role_service import RoleService


router = APIRouter(
    prefix="/establishments",
    tags=["roles"],
)


def get_role_service(
    session: AsyncSession = Depends(get_db),
) -> RoleService:
    return RoleService(
        role_repo=RoleRepository(session),
    )


@router.post(
    "/{establishment_id}/roles",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    establishment_id: uuid.UUID,
    data: RoleCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    role_service: RoleService = Depends(get_role_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.manage",
        establishment_id=establishment_id,
    )

    return await role_service.create_role(
        establishment_id=establishment_id,
        data=data,
    )


@router.get(
    "/{establishment_id}/roles",
    response_model=list[RoleRead],
)
async def list_roles(
    establishment_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    role_service: RoleService = Depends(get_role_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.manage",
        establishment_id=establishment_id,
    )

    return await role_service.list_roles(
        establishment_id=establishment_id,
    )


@router.get(
    "/{establishment_id}/roles/{role_id}",
    response_model=RoleRead,
)
async def get_role(
    establishment_id: uuid.UUID,
    role_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    role_service: RoleService = Depends(get_role_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.manage",
        establishment_id=establishment_id,
    )

    return await role_service.get_role(
        establishment_id=establishment_id,
        role_id=role_id,
    )


@router.patch(
    "/{establishment_id}/roles/{role_id}",
    response_model=RoleRead,
)
async def update_role(
    establishment_id: uuid.UUID,
    role_id: uuid.UUID,
    data: RoleUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    role_service: RoleService = Depends(get_role_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.manage",
        establishment_id=establishment_id,
    )

    return await role_service.update_role(
        establishment_id=establishment_id,
        role_id=role_id,
        data=data,
    )


@router.delete(
    "/{establishment_id}/roles/{role_id}",
    response_model=RoleRead,
)
async def delete_role(
    establishment_id: uuid.UUID,
    role_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    role_service: RoleService = Depends(get_role_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="role.manage",
        establishment_id=establishment_id,
    )

    return await role_service.delete_role(
        establishment_id=establishment_id,
        role_id=role_id,
    )


@router.post(
    "/sync-establishment-admin-permissions",
    status_code=status.HTTP_200_OK,
)
async def sync_establishment_admin_permissions(
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "organization.create",
    )

    return await rbac_service.sync_all_establishment_admin_permissions()