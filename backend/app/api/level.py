import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.student import LevelRepository
from app.schemas.student import LevelCreate, LevelRead, LevelUpdate
from app.services.level_service import LevelService
from app.services.rbac_service import RbacService


router = APIRouter(
    prefix="/levels",
    tags=["levels"],
)


def get_level_service(
    session: AsyncSession = Depends(get_db),
) -> LevelService:
    return LevelService(
        LevelRepository(session)
    )


@router.post(
    "",
    response_model=LevelRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_level(
    data: LevelCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    level_service: LevelService = Depends(get_level_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "level.create",
    )

    return await level_service.create_level(data)


@router.get(
    "",
    response_model=list[LevelRead],
)
async def list_levels(
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    level_service: LevelService = Depends(get_level_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "level.read",
    )

    return await level_service.list_levels()


@router.get(
    "/{level_id}",
    response_model=LevelRead,
)
async def get_level(
    level_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    level_service: LevelService = Depends(get_level_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "level.read",
    )

    return await level_service.get_level(level_id)


@router.patch(
    "/{level_id}",
    response_model=LevelRead,
)
async def update_level(
    level_id: uuid.UUID,
    data: LevelUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    level_service: LevelService = Depends(get_level_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "level.update",
    )

    return await level_service.update_level(
        level_id,
        data,
    )


@router.delete(
    "/{level_id}",
    response_model=LevelRead,
)
async def delete_level(
    level_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    level_service: LevelService = Depends(get_level_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "level.delete",
    )

    return await level_service.delete_level(level_id)