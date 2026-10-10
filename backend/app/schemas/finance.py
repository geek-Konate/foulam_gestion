import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.base import TimestampRead


class FeeTypeCreate(BaseModel):
    name: str
    amount: Decimal


class FeeTypeRead(TimestampRead):
    establishment_id: uuid.UUID
    name: str
    amount: Decimal

class FeeTypeUpdate(BaseModel):
    name: str
    amount: Decimal

class StudentFinancialSummary(BaseModel):
    student_id: uuid.UUID
    total_due: Decimal
    total_paid: Decimal
    remaining: Decimal

class PaymentCreate(BaseModel):
    student_id: uuid.UUID
    fee_type_id: uuid.UUID
    amount: Decimal
    payment_date: date
    payment_method: str
    created_by: uuid.UUID


class PaymentRead(TimestampRead):
    student_id: uuid.UUID
    fee_type_id: uuid.UUID
    amount: Decimal
    payment_date: date
    payment_method: str
    created_by: uuid.UUID


class ReceiptCreate(BaseModel):
    payment_id: uuid.UUID
    reference: str
    generated_at: datetime


class ReceiptRead(TimestampRead):
    payment_id: uuid.UUID
    reference: str
    generated_at: datetime