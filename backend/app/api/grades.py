import uuid

from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_current_user_id,
    get_rbac_service,
    get_grade_repository,
    get_evaluation_repository,
    get_student_repository,
    get_enrollment_repository,
    get_class_repository,
    get_academic_year_repository,
    get_teacher_assignment_repository,
    get_curriculum_subject_repository,
    get_user_repository,
)
from app.repositories.academic import GradeRepository, EvaluationRepository
from app.repositories.student import (
    StudentRepository,
    EnrollmentRepository,
    ClassRepository,
    AcademicYearRepository,
)
from app.repositories.curriculum import (
    TeacherAssignmentRepository,
    CurriculumSubjectRepository,
)
from app.repositories.rbac import UserRepository
from app.schemas.academic import (
    GradeCreate,
    GradeRead,
    GradeUpdate,
)
from app.services.grade_service import GradeService
from app.services.rbac_service import RbacService


router = APIRouter(
    prefix="/establishments",
    tags=["Grades"],
)


def get_grade_service(
    grade_repo: GradeRepository = Depends(
        get_grade_repository
    ),
    evaluation_repo: EvaluationRepository = Depends(
        get_evaluation_repository
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
    teacher_assignment_repo: TeacherAssignmentRepository = Depends(
        get_teacher_assignment_repository
    ),
    curriculum_subject_repo: CurriculumSubjectRepository = Depends(
        get_curriculum_subject_repository
    ),
    user_repo: UserRepository = Depends(
        get_user_repository
    ),
) -> GradeService:
    return GradeService(
        grade_repo=grade_repo,
        evaluation_repo=evaluation_repo,
        student_repo=student_repo,
        enrollment_repo=enrollment_repo,
        class_repo=class_repo,
        academic_year_repo=academic_year_repo,
        teacher_assignment_repo=teacher_assignment_repo,
        curriculum_subject_repo=curriculum_subject_repo,
        user_repo=user_repo,
    )


@router.post(
    "/{establishment_id}/grades",
    response_model=GradeRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_grade(
    establishment_id: uuid.UUID,
    data: GradeCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    grade_service: GradeService = Depends(get_grade_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "grade.create",
        establishment_id=establishment_id,
    )

    return await grade_service.create_grade(
        establishment_id=establishment_id,
        data=data,
        teacher_id=current_user_id,
    )


@router.get(
    "/{establishment_id}/evaluations/{evaluation_id}/grades",
    response_model=list[GradeRead],
)
async def list_evaluation_grades(
    establishment_id: uuid.UUID,
    evaluation_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    grade_service: GradeService = Depends(get_grade_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "grade.read",
        establishment_id=establishment_id,
    )

    return await grade_service.list_grades(
        establishment_id=establishment_id,
        evaluation_id=evaluation_id,
    )


@router.get(
    "/{establishment_id}/students/{student_id}/grades",
    response_model=list[GradeRead],
)
async def list_student_grades(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    grade_service: GradeService = Depends(get_grade_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "grade.read",
        establishment_id=establishment_id,
    )

    return await grade_service.list_student_grades(
        establishment_id=establishment_id,
        student_id=student_id,
    )


@router.get(
    "/{establishment_id}/grades/{grade_id}",
    response_model=GradeRead,
)
async def get_grade(
    establishment_id: uuid.UUID,
    grade_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    grade_service: GradeService = Depends(get_grade_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "grade.read",
        establishment_id=establishment_id,
    )

    return await grade_service.get_grade(
        establishment_id=establishment_id,
        grade_id=grade_id,
    )


@router.patch(
    "/{establishment_id}/grades/{grade_id}",
    response_model=GradeRead,
)
async def update_grade(
    establishment_id: uuid.UUID,
    grade_id: uuid.UUID,
    data: GradeUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    grade_service: GradeService = Depends(get_grade_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "grade.update",
        establishment_id=establishment_id,
    )

    return await grade_service.update_grade(
        establishment_id=establishment_id,
        grade_id=grade_id,
        data=data,
    )


@router.delete(
    "/{establishment_id}/grades/{grade_id}",
    response_model=GradeRead,
)
async def delete_grade(
    establishment_id: uuid.UUID,
    grade_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    grade_service: GradeService = Depends(get_grade_service),
):
    await rbac_service.require_permission(
        current_user_id,
        "grade.delete",
        establishment_id=establishment_id,
    )

    return await grade_service.delete_grade(
        establishment_id=establishment_id,
        grade_id=grade_id,
    )