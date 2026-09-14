import uuid

from sqlalchemy import select

from app.models.finance import FeeType, Payment, Receipt
from app.repositories.base import BaseRepository


class FeeTypeRepository(BaseRepository[FeeType]):
    model = FeeType

    async def get_by_establishment(self, establishment_id: uuid.UUID) -> list[FeeType]:
        stmt = select(FeeType).where(
            FeeType.establishment_id == establishment_id, FeeType.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class PaymentRepository(BaseRepository[Payment]):
    model = Payment

    async def get_by_student(self, student_id: uuid.UUID) -> list[Payment]:
        stmt = select(Payment).where(
            Payment.student_id == student_id, Payment.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class ReceiptRepository(BaseRepository[Receipt]):
    model = Receipt

    async def get_by_payment(self, payment_id: uuid.UUID) -> Receipt | None:
        stmt = select(Receipt).where(Receipt.payment_id == payment_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()