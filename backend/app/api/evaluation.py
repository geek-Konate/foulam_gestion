import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import (
    get_current_user_id,
    get_rbac_service,
    get_evaluation_repository,
    get_class_repository,
    get_academic_year_repository,
)
from app.repositories.academic import EvaluationRepository
from app.repositories.student import (
    ClassRepository,
    AcademicYearRepository,
)
from app.schemas.academic import (
    EvaluationCreate,
    EvaluationRead,
)
from app.services.evaluation_service import EvaluationService
from app.services.rbac_service import RbacService


router = APIRouter(
    prefix="/establishments",
    tags=["Evaluations"],
)


def get_evaluation_service(
    evaluation_repo: EvaluationRepository = Depends(
        get_evaluation_repository
    ),
    class_repo: ClassRepository = Depends(
        get_class_repository
    ),
    academic_year_repo: AcademicYearRepository = Depends(
        get_academic_year_repository
    ),
) -> EvaluationService:
    return EvaluationService(
        evaluation_repo=evaluation_repo,
        class_repo=class_repo,
        academic_year_repo=academic_year_repo,
    )


@router.post(
    "/{establishment_id}/evaluations",
    response_model=EvaluationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_evaluation(
    establishment_id: uuid.UUID,
    data: EvaluationCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    evaluation_service: EvaluationService = Depends(
        get_evaluation_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "evaluation.create",
        establishment_id=establishment_id,
    )

    return await evaluation_service.create_evaluation(
        establishment_id=establishment_id,
        data=data,
    )


@router.get(
    "/{establishment_id}/classes/{class_id}/evaluations",
    response_model=list[EvaluationRead],
)
async def list_evaluations(
    establishment_id: uuid.UUID,
    class_id: uuid.UUID,
    period: str | None = Query(default=None),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    evaluation_service: EvaluationService = Depends(
        get_evaluation_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "evaluation.read",
        establishment_id=establishment_id,
    )

    return await evaluation_service.list_evaluations(
        establishment_id=establishment_id,
        class_id=class_id,
        period=period,
    )


@router.get(
    "/{establishment_id}/evaluations/{evaluation_id}",
    response_model=EvaluationRead,
)
async def get_evaluation(
    establishment_id: uuid.UUID,
    evaluation_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    evaluation_service: EvaluationService = Depends(
        get_evaluation_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "evaluation.read",
        establishment_id=establishment_id,
    )

    return await evaluation_service.get_evaluation(
        establishment_id=establishment_id,
        evaluation_id=evaluation_id,
    )


@router.delete(
    "/{establishment_id}/evaluations/{evaluation_id}",
    response_model=EvaluationRead,
)
async def delete_evaluation(
    establishment_id: uuid.UUID,
    evaluation_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    evaluation_service: EvaluationService = Depends(
        get_evaluation_service
    ),
):
    await rbac_service.require_permission(
        current_user_id,
        "evaluation.delete",
        establishment_id=establishment_id,
    )

    return await evaluation_service.delete_evaluation(
        establishment_id=establishment_id,
        evaluation_id=evaluation_id,
    )