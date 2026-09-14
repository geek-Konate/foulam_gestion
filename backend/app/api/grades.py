import uuid

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id, get_grading_service
from app.schemas.academic import EvaluationCreate, EvaluationRead, GradeCreate, GradeRead, GradeUpdate
from app.services.grading_service import GradingService

router = APIRouter(prefix="/grades", tags=["grades"])


@router.post("/evaluations", response_model=EvaluationRead, status_code=201)
async def create_evaluation(
    data: EvaluationCreate,
    service: GradingService = Depends(get_grading_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return await service.create_evaluation(data, current_user_id)


@router.post("", response_model=GradeRead, status_code=201)
async def submit_grade(
    data: GradeCreate,
    service: GradingService = Depends(get_grading_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return await service.submit_grade(data, current_user_id)


@router.patch("/{grade_id}", response_model=GradeRead)
async def update_grade(
    grade_id: uuid.UUID,
    data: GradeUpdate,
    service: GradingService = Depends(get_grading_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return await service.update_grade(grade_id, data, current_user_id)