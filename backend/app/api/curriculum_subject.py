import uuid

from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_current_user_id,
    get_rbac_service,
    get_curriculum_subject_repository,
    get_curriculum_repository,
    get_subject_repository,
)
from app.repositories.curriculum import (
    CurriculumRepository,
    CurriculumSubjectRepository,
    SubjectRepository,
)
from app.schemas.curriculum import (
    CurriculumSubjectCreate,
    CurriculumSubjectRead,
)
from app.services.curriculum_subject_service import (
    CurriculumSubjectService,
)
from app.services.rbac_service import RbacService


router = APIRouter(
    prefix="/establishments",
    tags=["Curriculum Subjects"],
)


def get_curriculum_subject_service(
    curriculum_subject_repo: CurriculumSubjectRepository = Depends(
        get_curriculum_subject_repository
    ),
    curriculum_repo: CurriculumRepository = Depends(
        get_curriculum_repository
    ),
    subject_repo: SubjectRepository = Depends(
        get_subject_repository
    ),
) -> CurriculumSubjectService:
    return CurriculumSubjectService(
        curriculum_subject_repo=curriculum_subject_repo,
        curriculum_repo=curriculum_repo,
        subject_repo=subject_repo,
    )


@router.post(
    "/{establishment_id}/curriculums/{curriculum_id}/subjects/{subject_id}",
    response_model=CurriculumSubjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_subject_to_curriculum(
    establishment_id: uuid.UUID,
    curriculum_id: uuid.UUID,
    subject_id: uuid.UUID,
    data: CurriculumSubjectCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    curriculum_subject_service: CurriculumSubjectService = Depends(
        get_curriculum_subject_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.update",
        establishment_id=establishment_id,
    )

    return await curriculum_subject_service.add_subject(
        establishment_id=establishment_id,
        curriculum_id=curriculum_id,
        subject_id=subject_id,
        data=data,
    )


@router.get(
    "/{establishment_id}/curriculums/{curriculum_id}/subjects",
    response_model=list[CurriculumSubjectRead],
)
async def list_curriculum_subjects(
    establishment_id: uuid.UUID,
    curriculum_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    curriculum_subject_service: CurriculumSubjectService = Depends(
        get_curriculum_subject_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.read",
        establishment_id=establishment_id,
    )

    return await curriculum_subject_service.list_subjects(
        establishment_id=establishment_id,
        curriculum_id=curriculum_id,
    )


@router.delete(
    "/{establishment_id}/curriculums/{curriculum_id}/subjects/{subject_id}",
    response_model=CurriculumSubjectRead,
)
async def remove_subject_from_curriculum(
    establishment_id: uuid.UUID,
    curriculum_id: uuid.UUID,
    subject_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    curriculum_subject_service: CurriculumSubjectService = Depends(
        get_curriculum_subject_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.update",
        establishment_id=establishment_id,
    )

    return await curriculum_subject_service.remove_subject(
        establishment_id=establishment_id,
        curriculum_id=curriculum_id,
        subject_id=subject_id,
    )