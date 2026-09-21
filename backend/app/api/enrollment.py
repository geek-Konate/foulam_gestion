import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.student import (
    AcademicYearRepository,
    ClassRepository,
    EnrollmentRepository,
    StudentRepository,
)
from app.schemas.student import (
    EnrollmentCreate,
    EnrollmentRead,
    EnrollmentUpdate,
)
from app.services.enrollment_service import EnrollmentService
from app.services.rbac_service import RbacService


router = APIRouter(
    prefix="/establishments",
    tags=["enrollments"],
)


def get_enrollment_service(
    session: AsyncSession = Depends(get_db),
) -> EnrollmentService:
    return EnrollmentService(
        enrollment_repo=EnrollmentRepository(session),
        student_repo=StudentRepository(session),
        class_repo=ClassRepository(session),
        academic_year_repo=AcademicYearRepository(session),
    )


@router.post(
    "/{establishment_id}/enrollments",
    response_model=EnrollmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_enrollment(
    establishment_id: uuid.UUID,
    data: EnrollmentCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: EnrollmentService = Depends(get_enrollment_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "enrollment.create",
    )

    return await service.create_enrollment(
        establishment_id,
        data,
    )


@router.get(
    "/{establishment_id}/enrollments",
    response_model=list[EnrollmentRead],
)
async def list_enrollments(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID | None = None,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: EnrollmentService = Depends(get_enrollment_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "enrollment.read",
    )

    return await service.list_enrollments(
        establishment_id,
        student_id,
    )


@router.get(
    "/{establishment_id}/enrollments/{enrollment_id}",
    response_model=EnrollmentRead,
)
async def get_enrollment(
    establishment_id: uuid.UUID,
    enrollment_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: EnrollmentService = Depends(get_enrollment_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "enrollment.read",
    )

    return await service.get_enrollment(
        establishment_id,
        enrollment_id,
    )


@router.patch(
    "/{establishment_id}/enrollments/{enrollment_id}",
    response_model=EnrollmentRead,
)
async def update_enrollment(
    establishment_id: uuid.UUID,
    enrollment_id: uuid.UUID,
    data: EnrollmentUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: EnrollmentService = Depends(get_enrollment_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "enrollment.update",
    )

    return await service.update_enrollment(
        establishment_id,
        enrollment_id,
        data,
    )


@router.delete(
    "/{establishment_id}/enrollments/{enrollment_id}",
    response_model=EnrollmentRead,
)
async def delete_enrollment(
    establishment_id: uuid.UUID,
    enrollment_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: EnrollmentService = Depends(get_enrollment_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "enrollment.delete",
    )

    return await service.delete_enrollment(
        establishment_id,
        enrollment_id,
    )