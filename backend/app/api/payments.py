import uuid

from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_current_user,
    get_payment_repository,
    get_fee_type_repository,
    get_student_repository,
    require_organization_permission as require_permission,
)

from app.repositories.finance import (
    PaymentRepository,
    FeeTypeRepository,
)

from app.repositories.student import StudentRepository

from app.schemas.finance import (
    PaymentCreate,
    PaymentRead, StudentFinancialSummary,
)

from app.services.payment import PaymentService


router = APIRouter(
    tags=["Payments"],
)


def get_payment_service(
    payment_repo: PaymentRepository = Depends(
        get_payment_repository
    ),
    fee_type_repo: FeeTypeRepository = Depends(
        get_fee_type_repository
    ),
    student_repo: StudentRepository = Depends(
        get_student_repository
    ),
):
    return PaymentService(
        payment_repo=payment_repo,
        fee_type_repo=fee_type_repo,
        student_repo=student_repo,
    )


@router.post(
    "/establishments/{establishment_id}/payments",
    response_model=PaymentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    establishment_id: uuid.UUID,
    data: PaymentCreate,
    service: PaymentService = Depends(
        get_payment_service
    ),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("payment.create")),
):
    return await service.create(
        establishment_id=establishment_id,
        data=data,
        created_by=current_user.id,
    )


@router.get(
    "/establishments/{establishment_id}/payments/{payment_id}",
    response_model=PaymentRead,
)
async def get_payment(
    establishment_id: uuid.UUID,
    payment_id: uuid.UUID,
    service: PaymentService = Depends(
        get_payment_service
    ),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("payment.read")),
):
    return await service.get(
        establishment_id=establishment_id,
        payment_id=payment_id,
    )


@router.get(
    "/establishments/{establishment_id}/students/{student_id}/payments",
    response_model=list[PaymentRead],
)
async def list_student_payments(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    service: PaymentService = Depends(
        get_payment_service
    ),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("payment.read")),
):
    return await service.list_by_student(
        establishment_id=establishment_id,
        student_id=student_id,
    )


@router.get(
    "/establishments/{establishment_id}/fee-types/{fee_type_id}/payments",
    response_model=list[PaymentRead],
)
async def list_fee_type_payments(
    establishment_id: uuid.UUID,
    fee_type_id: uuid.UUID,
    service: PaymentService = Depends(
        get_payment_service
    ),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("payment.read")),
):
    return await service.list_by_fee_type(
        establishment_id=establishment_id,
        fee_type_id=fee_type_id,
    )


@router.delete(
    "/establishments/{establishment_id}/payments/{payment_id}",
    response_model=PaymentRead,
)
async def delete_payment(
    establishment_id: uuid.UUID,
    payment_id: uuid.UUID,
    service: PaymentService = Depends(
        get_payment_service
    ),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("payment.delete")),
):
    return await service.delete(
        establishment_id=establishment_id,
        payment_id=payment_id,
    )


@router.get(
    "/establishments/{establishment_id}/students/{student_id}/financial-summary",
    response_model=StudentFinancialSummary,
)
async def get_student_financial_summary(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    service: PaymentService = Depends(
        get_payment_service
    ),
    current_user=Depends(get_current_user),
    _=Depends(require_permission("payment.read")),
):
    return await service.financial_summary(
        establishment_id=establishment_id,
        student_id=student_id,
    )