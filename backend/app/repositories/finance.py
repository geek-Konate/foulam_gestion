import uuid
from decimal import Decimal

from sqlalchemy import func, select
from app.models.finance import FeeType, Payment, Receipt
from app.repositories.base import BaseRepository


class FeeTypeRepository(BaseRepository[FeeType]):
    model = FeeType

    async def get_by_name(
        self,
        establishment_id: uuid.UUID,
        name: str,
    ):
        stmt = select(FeeType).where(
            FeeType.establishment_id == establishment_id,
            FeeType.name == name,
            FeeType.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_establishment(
        self,
        establishment_id: uuid.UUID,
    ):
        stmt = (
            select(FeeType)
            .where(
                FeeType.establishment_id == establishment_id,
                FeeType.deleted_at.is_(None),
            )
            .order_by(FeeType.name)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_total_amount(
            self,
            establishment_id: uuid.UUID,
    ) -> Decimal:
        stmt = select(
            func.coalesce(
                func.sum(FeeType.amount),
                0,
            )
        ).where(
            FeeType.establishment_id == establishment_id,
            FeeType.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return Decimal(str(result.scalar_one()))


class PaymentRepository(BaseRepository[Payment]):
    model = Payment

    async def get_by_student(
        self,
        student_id: uuid.UUID,
    ):
        stmt = (
            select(Payment)
            .where(
                Payment.student_id == student_id,
                Payment.deleted_at.is_(None),
            )
            .order_by(Payment.payment_date.desc())
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_fee_type(
        self,
        fee_type_id: uuid.UUID,
    ):
        stmt = (
            select(Payment)
            .where(
                Payment.fee_type_id == fee_type_id,
                Payment.deleted_at.is_(None),
            )
            .order_by(Payment.payment_date.desc())
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_total_paid_by_student(
            self,
            student_id: uuid.UUID,
    ) -> Decimal:
        stmt = select(
            func.coalesce(
                func.sum(Payment.amount),
                0,
            )
        ).where(
            Payment.student_id == student_id,
            Payment.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return Decimal(str(result.scalar_one()))


class ReceiptRepository(BaseRepository[Receipt]):
    model = Receipt

    async def get_by_payment(
        self,
        payment_id: uuid.UUID,
    ):
        stmt = select(Receipt).where(
            Receipt.payment_id == payment_id,
            Receipt.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_reference(
        self,
        reference: str,
    ):
        stmt = select(Receipt).where(
            Receipt.reference == reference,
            Receipt.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()