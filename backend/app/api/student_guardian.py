import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.student import (
    GuardianRepository,
    StudentGuardianRepository,
    StudentRepository,
)
from app.schemas.student import StudentGuardianCreate, StudentGuardianRead
from app.services.rbac_service import RbacService
from app.services.student_guardian_service import StudentGuardianService


router = APIRouter(
    prefix="/establishments",
    tags=["student-guardians"],
)


def get_student_guardian_service(
    session: AsyncSession = Depends(get_db),
) -> StudentGuardianService:
    return StudentGuardianService(
        student_guardian_repo=StudentGuardianRepository(session),
        student_repo=StudentRepository(session),
        guardian_repo=GuardianRepository(session),
    )


@router.post(
    "/{establishment_id}/students/{student_id}/guardians",
    response_model=StudentGuardianRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_link(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    data: StudentGuardianCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: StudentGuardianService = Depends(
        get_student_guardian_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "guardian.create",
        establishment_id=establishment_id,
    )

    return await service.create_link(
        establishment_id,
        student_id,
        data,
    )


@router.get(
    "/{establishment_id}/students/{student_id}/guardians",
    response_model=list[StudentGuardianRead],
)
async def list_guardians(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: StudentGuardianService = Depends(
        get_student_guardian_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "guardian.read",
        establishment_id=establishment_id,
    )

    return await service.list_guardians(
        establishment_id,
        student_id,
    )


@router.delete(
    "/{establishment_id}/students/{student_id}/guardians/{guardian_id}",
    response_model=StudentGuardianRead,
)
async def delete_link(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    guardian_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: StudentGuardianService = Depends(
        get_student_guardian_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "guardian.delete",
        establishment_id=establishment_id,
    )

    return await service.delete_link(
        establishment_id,
        student_id,
        guardian_id,
    )