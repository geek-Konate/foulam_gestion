import uuid
from datetime import date

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class AcademicYear(BaseModel):
    __tablename__ = "academic_years"

    establishment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("establishments.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)  # ex: "2026-2027"
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

    classes: Mapped[list["Class"]] = relationship(back_populates="academic_year")


class Level(BaseModel):
    __tablename__ = "levels"

    name: Mapped[str] = mapped_column(String(50), nullable=False)  # CP, CM2, 6ème...
    category: Mapped[str] = mapped_column(String(50), nullable=False)


class Class(BaseModel):
    __tablename__ = "classes"

    academic_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("academic_years.id"), nullable=False
    )
    level_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("levels.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)  # CM2 A
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=30)

    academic_year: Mapped["AcademicYear"] = relationship(back_populates="classes")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="class_")


class Student(BaseModel):
    __tablename__ = "students"

    establishment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("establishments.id"),
        nullable=False,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    photo: Mapped[str | None] = mapped_column(String(255), nullable=True)

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="student"
    )

    student_guardians: Mapped[list["StudentGuardian"]] = relationship(
        back_populates="student"
    )


class Guardian(BaseModel):
    __tablename__ = "guardians"

    establishment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("establishments.id"),
        nullable=False,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)

    student_guardians: Mapped[list["StudentGuardian"]] = relationship(
        back_populates="guardian"
    )


class StudentGuardian(BaseModel):
    __tablename__ = "student_guardians"

    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    guardian_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("guardians.id"), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False)  # père, mère, tuteur...

    student: Mapped["Student"] = relationship(back_populates="student_guardians")
    guardian: Mapped["Guardian"] = relationship(back_populates="student_guardians")


class Enrollment(BaseModel):
    __tablename__ = "enrollments"

    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    class_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    enrollment_date: Mapped[date] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

    student: Mapped["Student"] = relationship(back_populates="enrollments")
    class_: Mapped["Class"] = relationship(back_populates="enrollments")