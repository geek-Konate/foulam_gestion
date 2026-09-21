import uuid
from decimal import Decimal

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.finance import PaymentRepository, FeeTypeRepository
from app.repositories.student import StudentRepository


class PaymentService:

    def __init__(
        self,
        payment_repo: PaymentRepository,
        fee_type_repo: FeeTypeRepository,
        student_repo: StudentRepository,
    ):
        self.payment_repo = payment_repo
        self.fee_type_repo = fee_type_repo
        self.student_repo = student_repo

    async def _get_student(
        self,
        establishment_id: uuid.UUID,
        student_id: uuid.UUID,
    ):
        student = await self.student_repo.get(student_id)

        if not student:
            raise NotFoundException(
                "Élève introuvable"
            )

        if student.establishment_id != establishment_id:
            raise NotFoundException(
                "Élève introuvable"
            )

        return student

    async def _get_fee_type(
        self,
        establishment_id: uuid.UUID,
        fee_type_id: uuid.UUID,
    ):
        fee_type = await self.fee_type_repo.get(fee_type_id)

        if not fee_type:
            raise NotFoundException(
                "Type de frais introuvable"
            )

        if fee_type.establishment_id != establishment_id:
            raise NotFoundException(
                "Type de frais introuvable"
            )

        return fee_type

    async def create(
        self,
        establishment_id: uuid.UUID,
        data,
        created_by: uuid.UUID,
    ):
        if data.amount <= 0:
            raise ConflictException(
                "Le montant du paiement doit être supérieur à zéro"
            )

        await self._get_student(
            establishment_id,
            data.student_id,
        )

        fee_type = await self._get_fee_type(
            establishment_id,
            data.fee_type_id,
        )

        if data.amount > fee_type.amount:
            raise ConflictException(
                "Le montant du paiement ne peut pas dépasser "
                "le montant du type de frais"
            )

        payment = await self.payment_repo.create(
            {
                "student_id": data.student_id,
                "fee_type_id": data.fee_type_id,
                "amount": data.amount,
                "payment_date": data.payment_date,
                "payment_method": data.payment_method,
                "created_by": created_by,
            }
        )

        return payment

    async def get(
        self,
        establishment_id: uuid.UUID,
        payment_id: uuid.UUID,
    ):
        payment = await self.payment_repo.get(payment_id)

        if not payment:
            raise NotFoundException(
                "Paiement introuvable"
            )

        await self._get_student(
            establishment_id,
            payment.student_id,
        )

        await self._get_fee_type(
            establishment_id,
            payment.fee_type_id,
        )

        return payment

    async def list_by_student(
        self,
        establishment_id: uuid.UUID,
        student_id: uuid.UUID,
    ):
        await self._get_student(
            establishment_id,
            student_id,
        )

        return await self.payment_repo.get_by_student(
            student_id
        )

    async def list_by_fee_type(
        self,
        establishment_id: uuid.UUID,
        fee_type_id: uuid.UUID,
    ):
        await self._get_fee_type(
            establishment_id,
            fee_type_id,
        )

        return await self.payment_repo.get_by_fee_type(
            fee_type_id
        )

    async def delete(
        self,
        establishment_id: uuid.UUID,
        payment_id: uuid.UUID,
    ):
        payment = await self.get(
            establishment_id,
            payment_id,
        )

        return await self.payment_repo.soft_delete(
            payment
        )

    async def financial_summary(
            self,
            establishment_id: uuid.UUID,
            student_id: uuid.UUID,
    ):
        student = await self.student_repo.get(student_id)

        if not student:
            raise NotFoundException(
                "Élève introuvable"
            )

        if student.establishment_id != establishment_id:
            raise NotFoundException(
                "Élève introuvable"
            )

        total_due = await self.fee_type_repo.get_total_amount(
            establishment_id
        )

        total_paid = await self.payment_repo.get_total_paid_by_student(
            student_id
        )

        remaining = total_due - total_paid

        if remaining < 0:
            remaining = Decimal("0")

        return {
            "student_id": student_id,
            "total_due": total_due,
            "total_paid": total_paid,
            "remaining": remaining,
        }