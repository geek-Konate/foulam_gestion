import uuid

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id, get_payment_service
from app.schemas.finance import FeeTypeCreate, FeeTypeRead, PaymentCreate, PaymentRead
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/fee-types", response_model=FeeTypeRead, status_code=201)
async def create_fee_type(
    data: FeeTypeCreate,
    service: PaymentService = Depends(get_payment_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return await service.create_fee_type(data, current_user_id)


@router.post("", response_model=PaymentRead, status_code=201)
async def record_payment(
    data: PaymentCreate,
    service: PaymentService = Depends(get_payment_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return await service.record_payment(data, current_user_id)


@router.get("/students/{student_id}", response_model=list[PaymentRead])
async def get_payment_history(
    student_id: uuid.UUID,
    service: PaymentService = Depends(get_payment_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return await service.get_payment_history(student_id, current_user_id)