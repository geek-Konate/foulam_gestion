import uuid

from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_current_user_id,
    get_fee_type_repository,
    get_rbac_service,
)

from app.repositories.finance import FeeTypeRepository

from app.schemas.finance import (
    FeeTypeCreate,
    FeeTypeRead,
    FeeTypeUpdate,
)

from app.services.fee_type import FeeTypeService
from app.services.rbac_service import RbacService


router = APIRouter(
   
    tags=["Fee Type"],
)


def get_fee_type_service(
    fee_type_repo: FeeTypeRepository = Depends(
        get_fee_type_repository
    ),
):
    return FeeTypeService(
        fee_type_repo=fee_type_repo
    )


@router.post(
    "/establishments/{establishment_id}/fee-types",
    response_model=FeeTypeRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_fee_type(
    establishment_id: uuid.UUID,
    data: FeeTypeCreate,
    service: FeeTypeService = Depends(
        get_fee_type_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="fee_type.create",
        establishment_id=establishment_id,
    )

    return await service.create(
        establishment_id=establishment_id,
        data=data,
    )


@router.get(
    "/establishments/{establishment_id}/fee-types",
    response_model=list[FeeTypeRead],
)
async def list_fee_types(
    establishment_id: uuid.UUID,
    service: FeeTypeService = Depends(
        get_fee_type_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="fee_type.read",
        establishment_id=establishment_id,
    )

    return await service.list(
        establishment_id=establishment_id,
    )


@router.get(
    "/establishments/{establishment_id}/fee-types/{fee_type_id}",
    response_model=FeeTypeRead,
)
async def get_fee_type(
    establishment_id: uuid.UUID,
    fee_type_id: uuid.UUID,
    service: FeeTypeService = Depends(
        get_fee_type_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="fee_type.read",
        establishment_id=establishment_id,
    )

    return await service.get(
        establishment_id=establishment_id,
        fee_type_id=fee_type_id,
    )


@router.patch(
    "/establishments/{establishment_id}/fee-types/{fee_type_id}",
    response_model=FeeTypeRead,
)
async def update_fee_type(
    establishment_id: uuid.UUID,
    fee_type_id: uuid.UUID,
    data: FeeTypeUpdate,
    service: FeeTypeService = Depends(
        get_fee_type_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="fee_type.update",
        establishment_id=establishment_id,
    )

    return await service.update(
        establishment_id=establishment_id,
        fee_type_id=fee_type_id,
        data=data,
    )


@router.delete(
    "/establishments/{establishment_id}/fee-types/{fee_type_id}",
    response_model=FeeTypeRead,
)
async def delete_fee_type(
    establishment_id: uuid.UUID,
    fee_type_id: uuid.UUID,
    service: FeeTypeService = Depends(
        get_fee_type_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="fee_type.delete",
        establishment_id=establishment_id,
    )

    return await service.delete(
        establishment_id=establishment_id,
        fee_type_id=fee_type_id,
    )