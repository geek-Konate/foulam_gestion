import uuid
from datetime import date as date_type, datetime

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class FeeType(BaseModel):
    __tablename__ = "fee_types"

    establishment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("establishments.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    payments: Mapped[list["Payment"]] = relationship(back_populates="fee_type")


class Payment(BaseModel):
    __tablename__ = "payments"

    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    fee_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("fee_types.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    payment_date: Mapped[date_type] = mapped_column(nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    fee_type: Mapped["FeeType"] = relationship(back_populates="payments")
    receipt: Mapped["Receipt"] = relationship(back_populates="payment", uselist=False)


class Receipt(BaseModel):
    __tablename__ = "receipts"

    payment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("payments.id"), unique=True, nullable=False
    )
    reference: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(nullable=False)

    payment: Mapped["Payment"] = relationship(back_populates="receipt")