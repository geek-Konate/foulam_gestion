import uuid
from datetime import date as date_type, datetime

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Evaluation(BaseModel):
    __tablename__ = "evaluations"

    class_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    date: Mapped[date_type] = mapped_column(nullable=False)

    grades: Mapped[list["Grade"]] = relationship(back_populates="evaluation")


class Grade(BaseModel):
    __tablename__ = "grades"

    evaluation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("evaluations.id"), nullable=False
    )
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    teacher_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)
    comment: Mapped[str | None] = mapped_column(String(255), nullable=True)

    evaluation: Mapped["Evaluation"] = relationship(back_populates="grades")


class Attendance(BaseModel):
    __tablename__ = "attendance"

    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    class_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    date: Mapped[date_type] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # présent, absent, retard
    remark: Mapped[str | None] = mapped_column(String(255), nullable=True)


class ReportCard(BaseModel):
    __tablename__ = "report_cards"

    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    academic_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("academic_years.id"), nullable=False
    )
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(nullable=False)