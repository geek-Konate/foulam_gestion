import uuid

from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_current_user_id,
    get_receipt_repository,
    get_payment_repository,
    get_student_repository,
    get_rbac_service,
)

from app.repositories.finance import (
    ReceiptRepository,
    PaymentRepository,
)

from app.repositories.student import StudentRepository

from app.schemas.finance import (
    ReceiptCreate,
    ReceiptRead,
)

from app.services.receipt import ReceiptService
from app.services.rbac_service import RbacService


router = APIRouter()


def get_receipt_service(
    receipt_repo: ReceiptRepository = Depends(
        get_receipt_repository
    ),
    payment_repo: PaymentRepository = Depends(
        get_payment_repository
    ),
    student_repo: StudentRepository = Depends(
        get_student_repository
    ),
):
    return ReceiptService(
        receipt_repo=receipt_repo,
        payment_repo=payment_repo,
        student_repo=student_repo,
    )


@router.post(
    "/establishments/{establishment_id}/receipts",
    response_model=ReceiptRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_receipt(
    establishment_id: uuid.UUID,
    data: ReceiptCreate,
    service: ReceiptService = Depends(
        get_receipt_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="receipt.create",
        establishment_id=establishment_id,
    )

    return await service.create(
        establishment_id=establishment_id,
        data=data,
    )


@router.get(
    "/establishments/{establishment_id}/receipts/{receipt_id}",
    response_model=ReceiptRead,
)
async def get_receipt(
    establishment_id: uuid.UUID,
    receipt_id: uuid.UUID,
    service: ReceiptService = Depends(
        get_receipt_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="receipt.read",
        establishment_id=establishment_id,
    )

    return await service.get(
        establishment_id=establishment_id,
        receipt_id=receipt_id,
    )


@router.get(
    "/establishments/{establishment_id}/payments/{payment_id}/receipt",
    response_model=ReceiptRead,
)
async def get_payment_receipt(
    establishment_id: uuid.UUID,
    payment_id: uuid.UUID,
    service: ReceiptService = Depends(
        get_receipt_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="receipt.read",
        establishment_id=establishment_id,
    )

    return await service.get_by_payment(
        establishment_id=establishment_id,
        payment_id=payment_id,
    )


@router.delete(
    "/establishments/{establishment_id}/receipts/{receipt_id}",
    response_model=ReceiptRead,
)
async def delete_receipt(
    establishment_id: uuid.UUID,
    receipt_id: uuid.UUID,
    service: ReceiptService = Depends(
        get_receipt_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="receipt.delete",
        establishment_id=establishment_id,
    )

    return await service.delete(
        establishment_id=establishment_id,
        receipt_id=receipt_id,
    )