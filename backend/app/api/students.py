import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.student import StudentRepository
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate
from app.services.rbac_service import RbacService
from app.services.student_service import StudentService


router = APIRouter(
    prefix="/establishments",
    tags=["students"],
)


def get_student_service(
    session: AsyncSession = Depends(get_db),
) -> StudentService:
    return StudentService(
        student_repo=StudentRepository(session),
    )


@router.post(
    "/{establishment_id}/students",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(
    establishment_id: uuid.UUID,
    data: StudentCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    student_service: StudentService = Depends(get_student_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "student.create",
        establishment_id=establishment_id,
    )

    return await student_service.create_student(
        establishment_id,
        data,
    )


@router.get(
    "/{establishment_id}/students",
    response_model=list[StudentRead],
)
async def list_students(
    establishment_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    student_service: StudentService = Depends(get_student_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "student.read",
        establishment_id=establishment_id,
    )

    return await student_service.list_students(
        establishment_id,
    )


@router.get(
    "/{establishment_id}/students/{student_id}",
    response_model=StudentRead,
)
async def get_student(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    student_service: StudentService = Depends(get_student_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "student.read",
        establishment_id=establishment_id,
    )

    return await student_service.get_student(
        establishment_id,
        student_id,
    )


@router.patch(
    "/{establishment_id}/students/{student_id}",
    response_model=StudentRead,
)
async def update_student(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    data: StudentUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    student_service: StudentService = Depends(get_student_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "student.update",
        establishment_id=establishment_id,
    )

    return await student_service.update_student(
        establishment_id,
        student_id,
        data,
    )


@router.delete(
    "/{establishment_id}/students/{student_id}",
    response_model=StudentRead,
)
async def delete_student(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    student_service: StudentService = Depends(get_student_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "student.delete",
        establishment_id=establishment_id,
    )

    return await student_service.delete_student(
        establishment_id,
        student_id,
    )