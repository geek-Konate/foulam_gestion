import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.student import (
    AcademicYearRepository,
    ClassRepository,
    LevelRepository,
)
from app.schemas.student import ClassCreate, ClassRead, ClassUpdate
from app.services.class_service import ClassService
from app.services.rbac_service import RbacService


router = APIRouter(
    prefix="/establishments",
    tags=["classes"],
)


def get_class_service(
    session: AsyncSession = Depends(get_db),
) -> ClassService:
    return ClassService(
        class_repo=ClassRepository(session),
        academic_year_repo=AcademicYearRepository(session),
        level_repo=LevelRepository(session),
    )


@router.post(
    "/{establishment_id}/classes",
    response_model=ClassRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_class(
    establishment_id: uuid.UUID,
    data: ClassCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    class_service: ClassService = Depends(get_class_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "class.create",
    )

    return await class_service.create_class(
        establishment_id,
        data,
    )


@router.get(
    "/{establishment_id}/classes",
    response_model=list[ClassRead],
)
async def list_classes(
    establishment_id: uuid.UUID,
    academic_year_id: uuid.UUID | None = None,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    class_service: ClassService = Depends(get_class_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "class.read",
    )

    return await class_service.list_classes(
        establishment_id,
        academic_year_id,
    )


@router.get(
    "/{establishment_id}/classes/{class_id}",
    response_model=ClassRead,
)
async def get_class(
    establishment_id: uuid.UUID,
    class_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    class_service: ClassService = Depends(get_class_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "class.read",
    )

    return await class_service.get_class(
        establishment_id,
        class_id,
    )


@router.patch(
    "/{establishment_id}/classes/{class_id}",
    response_model=ClassRead,
)
async def update_class(
    establishment_id: uuid.UUID,
    class_id: uuid.UUID,
    data: ClassUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    class_service: ClassService = Depends(get_class_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "class.update",
    )

    return await class_service.update_class(
        establishment_id,
        class_id,
        data,
    )


@router.delete(
    "/{establishment_id}/classes/{class_id}",
    response_model=ClassRead,
)
async def delete_class(
    establishment_id: uuid.UUID,
    class_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    class_service: ClassService = Depends(get_class_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "class.delete",
    )

    return await class_service.delete_class(
        establishment_id,
        class_id,
    )