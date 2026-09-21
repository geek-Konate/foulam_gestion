import uuid
from decimal import Decimal

from pydantic import BaseModel


class EstablishmentDashboardRead(BaseModel):
    establishment_id: uuid.UUID

    academic_year_id: uuid.UUID | None
    academic_year_name: str | None

    students_count: int
    classes_count: int
    teachers_count: int

    total_due: Decimal
    total_paid: Decimal
    remaining: Decimal


class TeacherAssignmentDashboardRead(BaseModel):
    assignment_id: uuid.UUID
    class_id: uuid.UUID
    curriculum_subject_id: uuid.UUID


class TeacherDashboardRead(BaseModel):
    teacher_id: uuid.UUID
    establishment_id: uuid.UUID

    assignments_count: int
    classes_count: int
    evaluations_count: int

    assignments: list[TeacherAssignmentDashboardRead]