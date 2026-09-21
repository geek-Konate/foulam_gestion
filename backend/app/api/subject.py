import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.curriculum import SubjectRepository
from app.schemas.curriculum import (
    SubjectCreate,
    SubjectRead,
    SubjectUpdate,
)
from app.services.rbac_service import RbacService
from app.services.subject_service import SubjectService


router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
)


def get_subject_service(
    session: AsyncSession = Depends(get_db),
) -> SubjectService:
    return SubjectService(
        subject_repo=SubjectRepository(session),
    )


@router.post(
    "",
    response_model=SubjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_subject(
    data: SubjectCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: SubjectService = Depends(get_subject_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "subject.create",
    )

    return await service.create_subject(data)


@router.get(
    "",
    response_model=list[SubjectRead],
)
async def list_subjects(
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: SubjectService = Depends(get_subject_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "subject.read",
    )

    return await service.list_subjects()


@router.get(
    "/{subject_id}",
    response_model=SubjectRead,
)
async def get_subject(
    subject_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: SubjectService = Depends(get_subject_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "subject.read",
    )

    return await service.get_subject(subject_id)


@router.patch(
    "/{subject_id}",
    response_model=SubjectRead,
)
async def update_subject(
    subject_id: uuid.UUID,
    data: SubjectUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: SubjectService = Depends(get_subject_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "subject.update",
    )

    return await service.update_subject(
        subject_id,
        data,
    )


@router.delete(
    "/{subject_id}",
    response_model=SubjectRead,
)
async def delete_subject(
    subject_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: SubjectService = Depends(get_subject_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "subject.delete",
    )

    return await service.delete_subject(subject_id)