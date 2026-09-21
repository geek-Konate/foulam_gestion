import uuid

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import (
    get_current_user_id,
    get_rbac_service,
)
from app.schemas.curriculum import (
    CurriculumCreate,
    CurriculumRead,
    CurriculumUpdate,
)
from app.services.curriculum_service import CurriculumService
from app.services.rbac_service import RbacService
from app.repositories.curriculum import CurriculumRepository
from app.repositories.student import AcademicYearRepository
from app.repositories.student import LevelRepository
from app.api.deps import (
    get_curriculum_repository,
    get_academic_year_repository,
    get_level_repository,
)


router = APIRouter(
    prefix="/establishments",
    tags=["Curriculums"],
)


def get_curriculum_service(
    curriculum_repo: CurriculumRepository = Depends(
        get_curriculum_repository
    ),
    academic_year_repo: AcademicYearRepository = Depends(
        get_academic_year_repository
    ),
    level_repo: LevelRepository = Depends(
        get_level_repository
    ),
) -> CurriculumService:
    return CurriculumService(
        curriculum_repo=curriculum_repo,
        academic_year_repo=academic_year_repo,
        level_repo=level_repo,
    )


@router.post(
    "/{establishment_id}/curriculums",
    response_model=CurriculumRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_curriculum(
    establishment_id: uuid.UUID,
    data: CurriculumCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    curriculum_service: CurriculumService = Depends(
        get_curriculum_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.create",
        establishment_id=establishment_id,
    )

    return await curriculum_service.create_curriculum(
        establishment_id,
        data,
    )


@router.get(
    "/{establishment_id}/curriculums",
    response_model=list[CurriculumRead],
)
async def list_curriculums(
    establishment_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    curriculum_service: CurriculumService = Depends(
        get_curriculum_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.read",
        establishment_id=establishment_id,
    )

    return await curriculum_service.list_curriculums(
        establishment_id
    )


@router.get(
    "/{establishment_id}/curriculums/{curriculum_id}",
    response_model=CurriculumRead,
)
async def get_curriculum(
    establishment_id: uuid.UUID,
    curriculum_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    curriculum_service: CurriculumService = Depends(
        get_curriculum_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.read",
        establishment_id=establishment_id,
    )

    return await curriculum_service.get_curriculum(
        establishment_id,
        curriculum_id,
    )


@router.patch(
    "/{establishment_id}/curriculums/{curriculum_id}",
    response_model=CurriculumRead,
)
async def update_curriculum(
    establishment_id: uuid.UUID,
    curriculum_id: uuid.UUID,
    data: CurriculumUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    curriculum_service: CurriculumService = Depends(
        get_curriculum_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.update",
        establishment_id=establishment_id,
    )

    return await curriculum_service.update_curriculum(
        establishment_id,
        curriculum_id,
        data,
    )


@router.delete(
    "/{establishment_id}/curriculums/{curriculum_id}",
    response_model=CurriculumRead,
)
async def delete_curriculum(
    establishment_id: uuid.UUID,
    curriculum_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    curriculum_service: CurriculumService = Depends(
        get_curriculum_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "curriculum.delete",
        establishment_id=establishment_id,
    )

    return await curriculum_service.delete_curriculum(
        establishment_id,
        curriculum_id,
    )