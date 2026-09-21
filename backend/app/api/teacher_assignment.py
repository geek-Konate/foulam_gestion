import uuid

from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_current_user_id,
    get_rbac_service,

    get_class_curriculum_repository,
    get_curriculum_subject_repository,
    get_class_repository,

    get_academic_year_repository, get_teacher_assignment_repository, get_user_repository,
)
from app.repositories.curriculum import (
    TeacherAssignmentRepository,
    ClassCurriculumRepository,
    CurriculumSubjectRepository,
)
from app.repositories.student import (
    ClassRepository,
    AcademicYearRepository,
)
from app.repositories.rbac import UserRepository
from app.schemas.curriculum import TeacherAssignmentRead
from app.services.teacher_assignment_service import TeacherAssignmentService
from app.services.rbac_service import RbacService


router = APIRouter(
    prefix="/establishments",
    tags=["Teacher Assignments"],
)


def get_teacher_assignment_service(
    teacher_assignment_repo: TeacherAssignmentRepository = Depends(
        get_teacher_assignment_repository
    ),
    class_curriculum_repo: ClassCurriculumRepository = Depends(
        get_class_curriculum_repository
    ),
    curriculum_subject_repo: CurriculumSubjectRepository = Depends(
        get_curriculum_subject_repository
    ),
    class_repo: ClassRepository = Depends(
        get_class_repository
    ),
    user_repo: UserRepository = Depends(
        get_user_repository
    ),
    academic_year_repo: AcademicYearRepository = Depends(
        get_academic_year_repository
    ),
) -> TeacherAssignmentService:
    return TeacherAssignmentService(
        teacher_assignment_repo=teacher_assignment_repo,
        class_curriculum_repo=class_curriculum_repo,
        curriculum_subject_repo=curriculum_subject_repo,
        class_repo=class_repo,
        user_repo=user_repo,
        academic_year_repo=academic_year_repo,
    )


@router.post(
    "/{establishment_id}/classes/{class_id}/curriculum-subjects/{curriculum_subject_id}/teachers/{user_id}",
    response_model=TeacherAssignmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def assign_teacher(
    establishment_id: uuid.UUID,
    class_id: uuid.UUID,
    curriculum_subject_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    teacher_assignment_service: TeacherAssignmentService = Depends(
        get_teacher_assignment_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "teacher_assignment.create",
        establishment_id=establishment_id,
    )

    return await teacher_assignment_service.assign_teacher(
        establishment_id=establishment_id,
        class_id=class_id,
        curriculum_subject_id=curriculum_subject_id,
        user_id=user_id,
    )


@router.get(
    "/{establishment_id}/classes/{class_id}/teacher-assignments",
    response_model=list[TeacherAssignmentRead],
)
async def list_class_teacher_assignments(
    establishment_id: uuid.UUID,
    class_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    teacher_assignment_service: TeacherAssignmentService = Depends(
        get_teacher_assignment_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "teacher_assignment.read",
        establishment_id=establishment_id,
    )

    return await teacher_assignment_service.list_by_class(
        establishment_id=establishment_id,
        class_id=class_id,
    )


@router.get(
    "/{establishment_id}/teachers/{user_id}/assignments",
    response_model=list[TeacherAssignmentRead],
)
async def list_teacher_assignments(
    establishment_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    teacher_assignment_service: TeacherAssignmentService = Depends(
        get_teacher_assignment_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "teacher_assignment.read",
        establishment_id=establishment_id,
    )

    return await teacher_assignment_service.list_by_teacher(
        establishment_id=establishment_id,
        user_id=user_id,
    )


@router.delete(
    "/{establishment_id}/teacher-assignments/{assignment_id}",
    response_model=TeacherAssignmentRead,
)
async def delete_teacher_assignment(
    establishment_id: uuid.UUID,
    assignment_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    teacher_assignment_service: TeacherAssignmentService = Depends(
        get_teacher_assignment_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "teacher_assignment.delete",
        establishment_id=establishment_id,
    )

    return await teacher_assignment_service.delete_assignment(
        establishment_id=establishment_id,
        assignment_id=assignment_id,
    )