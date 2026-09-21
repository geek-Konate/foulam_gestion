import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.finance import (
    ReceiptRepository,
    PaymentRepository,
)
from app.repositories.student import StudentRepository


class ReceiptService:

    def __init__(
        self,
        receipt_repo: ReceiptRepository,
        payment_repo: PaymentRepository,
        student_repo: StudentRepository,
    ):
        self.receipt_repo = receipt_repo
        self.payment_repo = payment_repo
        self.student_repo = student_repo

    async def _get_payment(
        self,
        establishment_id: uuid.UUID,
        payment_id: uuid.UUID,
    ):
        payment = await self.payment_repo.get(payment_id)

        if not payment:
            raise NotFoundException(
                "Paiement introuvable"
            )

        student = await self.student_repo.get(
            payment.student_id
        )

        if not student:
            raise NotFoundException(
                "Paiement introuvable"
            )

        if student.establishment_id != establishment_id:
            raise NotFoundException(
                "Paiement introuvable"
            )

        return payment

    async def create(
        self,
        establishment_id: uuid.UUID,
        data,
    ):
        payment = await self._get_payment(
            establishment_id,
            data.payment_id,
        )

        existing = await self.receipt_repo.get_by_payment(
            data.payment_id
        )

        if existing:
            raise ConflictException(
                "Un reçu existe déjà pour ce paiement"
            )

        existing_reference = (
            await self.receipt_repo.get_by_reference(
                data.reference
            )
        )

        if existing_reference:
            raise ConflictException(
                "Cette référence de reçu existe déjà"
            )

        return await self.receipt_repo.create(
            {
                "payment_id": payment.id,
                "reference": data.reference,
                "generated_at": data.generated_at,
            }
        )

    async def get(
        self,
        establishment_id: uuid.UUID,
        receipt_id: uuid.UUID,
    ):
        receipt = await self.receipt_repo.get(
            receipt_id
        )

        if not receipt:
            raise NotFoundException(
                "Reçu introuvable"
            )

        await self._get_payment(
            establishment_id,
            receipt.payment_id,
        )

        return receipt

    async def get_by_payment(
        self,
        establishment_id: uuid.UUID,
        payment_id: uuid.UUID,
    ):
        await self._get_payment(
            establishment_id,
            payment_id,
        )

        receipt = await self.receipt_repo.get_by_payment(
            payment_id
        )

        if not receipt:
            raise NotFoundException(
                "Reçu introuvable"
            )

        return receipt

    async def delete(
        self,
        establishment_id: uuid.UUID,
        receipt_id: uuid.UUID,
    ):
        receipt = await self.get(
            establishment_id,
            receipt_id,
        )

        return await self.receipt_repo.soft_delete(
            receipt
        )