import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import (
    get_current_user_id,
    get_rbac_service,

    get_class_repository,
    get_academic_year_repository, get_attendance_repository, get_student_repository, get_enrollment_repository,
)
from app.repositories.academic import AttendanceRepository
from app.repositories.student import (
    StudentRepository,
    EnrollmentRepository,
    ClassRepository,
    AcademicYearRepository,
)
from app.schemas.academic import (
    AttendanceCreate,
    AttendanceRead,
    AttendanceUpdate,
)
from app.services.attendance_service import AttendanceService
from app.services.rbac_service import RbacService


router = APIRouter(
    prefix="/establishments",
    tags=["Attendance"],
)


def get_attendance_service(
    attendance_repo: AttendanceRepository = Depends(
        get_attendance_repository
    ),
    student_repo: StudentRepository = Depends(
        get_student_repository
    ),
    enrollment_repo: EnrollmentRepository = Depends(
        get_enrollment_repository
    ),
    class_repo: ClassRepository = Depends(
        get_class_repository
    ),
    academic_year_repo: AcademicYearRepository = Depends(
        get_academic_year_repository
    ),
) -> AttendanceService:
    return AttendanceService(
        attendance_repo=attendance_repo,
        student_repo=student_repo,
        enrollment_repo=enrollment_repo,
        class_repo=class_repo,
        academic_year_repo=academic_year_repo,
    )


@router.post(
    "/{establishment_id}/attendance",
    response_model=AttendanceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_attendance(
    establishment_id: uuid.UUID,
    data: AttendanceCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    attendance_service: AttendanceService = Depends(
        get_attendance_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "attendance.create",
        establishment_id=establishment_id,
    )

    return await attendance_service.create_attendance(
        establishment_id=establishment_id,
        data=data,
    )


@router.get(
    "/{establishment_id}/classes/{class_id}/attendance",
    response_model=list[AttendanceRead],
)
async def list_class_attendance(
    establishment_id: uuid.UUID,
    class_id: uuid.UUID,
    attendance_date: date = Query(...),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    attendance_service: AttendanceService = Depends(
        get_attendance_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "attendance.read",
        establishment_id=establishment_id,
    )

    return await attendance_service.list_by_class_and_date(
        establishment_id=establishment_id,
        class_id=class_id,
        attendance_date=attendance_date,
    )


@router.get(
    "/{establishment_id}/students/{student_id}/attendance",
    response_model=list[AttendanceRead],
)
async def list_student_attendance(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    attendance_service: AttendanceService = Depends(
        get_attendance_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "attendance.read",
        establishment_id=establishment_id,
    )

    return await attendance_service.list_by_student(
        establishment_id=establishment_id,
        student_id=student_id,
    )


@router.get(
    "/{establishment_id}/attendance/{attendance_id}",
    response_model=AttendanceRead,
)
async def get_attendance(
    establishment_id: uuid.UUID,
    attendance_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    attendance_service: AttendanceService = Depends(
        get_attendance_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "attendance.read",
        establishment_id=establishment_id,
    )

    return await attendance_service.get_attendance(
        establishment_id=establishment_id,
        attendance_id=attendance_id,
    )


@router.patch(
    "/{establishment_id}/attendance/{attendance_id}",
    response_model=AttendanceRead,
)
async def update_attendance(
    establishment_id: uuid.UUID,
    attendance_id: uuid.UUID,
    data: AttendanceUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    attendance_service: AttendanceService = Depends(
        get_attendance_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "attendance.update",
        establishment_id=establishment_id,
    )

    return await attendance_service.update_attendance(
        establishment_id=establishment_id,
        attendance_id=attendance_id,
        data=data,
    )


@router.delete(
    "/{establishment_id}/attendance/{attendance_id}",
    response_model=AttendanceRead,
)
async def delete_attendance(
    establishment_id: uuid.UUID,
    attendance_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    attendance_service: AttendanceService = Depends(
        get_attendance_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "attendance.delete",
        establishment_id=establishment_id,
    )

    return await attendance_service.delete_attendance(
        establishment_id=establishment_id,
        attendance_id=attendance_id,
    )