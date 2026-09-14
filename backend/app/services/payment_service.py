import uuid

from app.core.exceptions import NotFoundException
from app.repositories.finance import FeeTypeRepository, PaymentRepository, ReceiptRepository
from app.repositories.student import StudentRepository
from app.schemas.finance import FeeTypeCreate, PaymentCreate
from app.services.rbac_service import RbacService


class PaymentService:
    def __init__(
        self,
        fee_type_repo: FeeTypeRepository,
        payment_repo: PaymentRepository,
        receipt_repo: ReceiptRepository,
        student_repo: StudentRepository,
        rbac_service: RbacService,
    ):
        self.fee_type_repo = fee_type_repo
        self.payment_repo = payment_repo
        self.receipt_repo = receipt_repo
        self.student_repo = student_repo
        self.rbac_service = rbac_service

    async def create_fee_type(self, data: FeeTypeCreate, current_user_id: uuid.UUID):
        await self.rbac_service.require_permission(
            current_user_id, "fee_type.create", establishment_id=data.establishment_id
        )
        return await self.fee_type_repo.create(data.model_dump())

    async def record_payment(self, data: PaymentCreate, current_user_id: uuid.UUID):
        student = await self.student_repo.get(data.student_id)
        if not student:
            raise NotFoundException("Élève introuvable")

        fee_type = await self.fee_type_repo.get(data.fee_type_id)
        if not fee_type:
            raise NotFoundException("Type de frais introuvable")

        await self.rbac_service.require_permission(
            current_user_id, "payment.create", establishment_id=fee_type.establishment_id
        )

        payment = await self.payment_repo.create(data.model_dump())

        reference = f"RCT-{payment.id.hex[:10].upper()}"
        from datetime import datetime, timezone
        await self.receipt_repo.create({
            "payment_id": payment.id,
            "reference": reference,
            "generated_at": datetime.now(timezone.utc),
        })

        return payment

    async def get_payment_history(self, student_id: uuid.UUID, current_user_id: uuid.UUID):
        student = await self.student_repo.get(student_id)
        if not student:
            raise NotFoundException("Élève introuvable")

        payments = await self.payment_repo.get_by_student(student_id)
        if payments:
            fee_type = await self.fee_type_repo.get(payments[0].fee_type_id)
            await self.rbac_service.require_permission(
                current_user_id, "payment.read", establishment_id=fee_type.establishment_id
            )
        return payments