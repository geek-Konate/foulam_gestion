import uuid

from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_current_user_id,
    get_rbac_service,

    get_curriculum_repository,

    get_academic_year_repository, get_class_curriculum_repository, get_class_repository,
)
from app.repositories.curriculum import (
    ClassCurriculumRepository,
    CurriculumRepository,
)
from app.repositories.student import ClassRepository
from app.repositories.student import AcademicYearRepository
from app.services.class_curriculum_service import ClassCurriculumService
from app.services.rbac_service import RbacService
from app.schemas.curriculum import ClassCurriculumRead


router = APIRouter(
    prefix="/establishments",
    tags=["Class Curriculums"],
)


def get_class_curriculum_service(
    class_curriculum_repo: ClassCurriculumRepository = Depends(
        get_class_curriculum_repository
    ),
    curriculum_repo: CurriculumRepository = Depends(
        get_curriculum_repository
    ),
    class_repo: ClassRepository = Depends(
        get_class_repository
    ),
    academic_year_repo: AcademicYearRepository = Depends(
        get_academic_year_repository
    ),
) -> ClassCurriculumService:
    return ClassCurriculumService(
        class_curriculum_repo=class_curriculum_repo,
        curriculum_repo=curriculum_repo,
        class_repo=class_repo,
        academic_year_repo=academic_year_repo,
    )


@router.post(
    "/{establishment_id}/classes/{class_id}/curriculum/{curriculum_id}",
    response_model=ClassCurriculumRead,
    status_code=status.HTTP_201_CREATED,
)
async def assign_curriculum(
    establishment_id: uuid.UUID,
    class_id: uuid.UUID,
    curriculum_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    class_curriculum_service: ClassCurriculumService = Depends(
        get_class_curriculum_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.update",
        establishment_id=establishment_id,
    )

    return await class_curriculum_service.assign_curriculum(
        establishment_id=establishment_id,
        class_id=class_id,
        curriculum_id=curriculum_id,
    )


@router.get(
    "/{establishment_id}/classes/{class_id}/curriculum",
    response_model=ClassCurriculumRead,
)
async def get_class_curriculum(
    establishment_id: uuid.UUID,
    class_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    class_curriculum_service: ClassCurriculumService = Depends(
        get_class_curriculum_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.read",
        establishment_id=establishment_id,
    )

    return await class_curriculum_service.get_class_curriculum(
        establishment_id=establishment_id,
        class_id=class_id,
    )


@router.delete(
    "/{establishment_id}/classes/{class_id}/curriculum",
    response_model=ClassCurriculumRead,
)
async def remove_curriculum(
    establishment_id: uuid.UUID,
    class_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    class_curriculum_service: ClassCurriculumService = Depends(
        get_class_curriculum_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.update",
        establishment_id=establishment_id,
    )

    return await class_curriculum_service.remove_curriculum(
        establishment_id=establishment_id,
        class_id=class_id,
    )