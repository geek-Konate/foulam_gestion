import uuid

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_current_user_id, get_enrollment_service
from app.schemas.student import EnrollmentCreate, EnrollmentRead
from app.services.enrollment_service import EnrollmentService

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/enrollments", response_model=EnrollmentRead, status_code=201)
async def enroll_student(
    data: EnrollmentCreate,
    service: EnrollmentService = Depends(get_enrollment_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return await service.enroll_student(data, current_user_id)


@router.get("/{student_id}/enrollments", response_model=list[EnrollmentRead])
async def get_enrollment_history(
    student_id: uuid.UUID,
    service: EnrollmentService = Depends(get_enrollment_service),
    current_user=Depends(get_current_user),
):
    return await service.enrollment_repo.get_history_for_student(student_id)