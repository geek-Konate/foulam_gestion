import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.base import TimestampRead


class EvaluationCreate(BaseModel):
    class_id: uuid.UUID
    subject_id: uuid.UUID
    name: str
    period: str
    date: date


class EvaluationRead(TimestampRead):
    class_id: uuid.UUID
    subject_id: uuid.UUID
    name: str
    period: str
    date: date

    model_config = ConfigDict(from_attributes=True)
class GradeCreate(BaseModel):
    evaluation_id: uuid.UUID
    student_id: uuid.UUID
    teacher_id: uuid.UUID
    value: float = Field(ge=0, le=20)
    comment: str | None = None


class GradeUpdate(BaseModel):
    value: float | None = Field(default=None, ge=0, le=20)
    comment: str | None = None


class GradeRead(TimestampRead):
    evaluation_id: uuid.UUID
    student_id: uuid.UUID
    teacher_id: uuid.UUID
    value: float
    comment: str | None


class AttendanceCreate(BaseModel):
    student_id: uuid.UUID
    class_id: uuid.UUID
    date: date
    status: str
    remark: str | None = None


class AttendanceRead(TimestampRead):
    student_id: uuid.UUID
    class_id: uuid.UUID
    date: date
    status: str
    remark: str | None

class AttendanceUpdate(BaseModel):
    status: str | None = None
    remark: str | None = None

class ReportCardCreate(BaseModel):
    student_id: uuid.UUID
    academic_year_id: uuid.UUID
    period: str
    file_url: str
    generated_at: datetime


class ReportCardRead(TimestampRead):
    student_id: uuid.UUID
    academic_year_id: uuid.UUID
    period: str
    file_url: str
    generated_at: datetime