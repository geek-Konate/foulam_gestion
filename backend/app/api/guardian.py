import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.student import GuardianRepository
from app.schemas.student import GuardianCreate, GuardianRead, GuardianUpdate
from app.services.guardian_service import GuardianService
from app.services.rbac_service import RbacService


router = APIRouter(
    prefix="/establishments",
    tags=["guardians"],
)


def get_guardian_service(
    session: AsyncSession = Depends(get_db),
) -> GuardianService:
    return GuardianService(
        guardian_repo=GuardianRepository(session),
    )


@router.post(
    "/{establishment_id}/guardians",
    response_model=GuardianRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_guardian(
    establishment_id: uuid.UUID,
    data: GuardianCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    guardian_service: GuardianService = Depends(get_guardian_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "guardian.create",
        establishment_id=establishment_id,
    )

    return await guardian_service.create_guardian(
        establishment_id,
        data,
    )


@router.get(
    "/{establishment_id}/guardians",
    response_model=list[GuardianRead],
)
async def list_guardians(
    establishment_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    guardian_service: GuardianService = Depends(get_guardian_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "guardian.read",
        establishment_id=establishment_id,
    )

    return await guardian_service.list_guardians(
        establishment_id,
    )


@router.get(
    "/{establishment_id}/guardians/{guardian_id}",
    response_model=GuardianRead,
)
async def get_guardian(
    establishment_id: uuid.UUID,
    guardian_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    guardian_service: GuardianService = Depends(get_guardian_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "guardian.read",
        establishment_id=establishment_id,
    )

    return await guardian_service.get_guardian(
        establishment_id,
        guardian_id,
    )


@router.patch(
    "/{establishment_id}/guardians/{guardian_id}",
    response_model=GuardianRead,
)
async def update_guardian(
    establishment_id: uuid.UUID,
    guardian_id: uuid.UUID,
    data: GuardianUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    guardian_service: GuardianService = Depends(get_guardian_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "guardian.update",
        establishment_id=establishment_id,
    )

    return await guardian_service.update_guardian(
        establishment_id,
        guardian_id,
        data,
    )


@router.delete(
    "/{establishment_id}/guardians/{guardian_id}",
    response_model=GuardianRead,
)
async def delete_guardian(
    establishment_id: uuid.UUID,
    guardian_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    guardian_service: GuardianService = Depends(get_guardian_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "guardian.delete",
        establishment_id=establishment_id,
    )

    return await guardian_service.delete_guardian(
        establishment_id,
        guardian_id,
    )