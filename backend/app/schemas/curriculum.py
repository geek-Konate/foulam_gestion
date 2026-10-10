import uuid

from pydantic import BaseModel

from app.schemas.base import TimestampRead


class CurriculumCreate(BaseModel):
    establishment_id: uuid.UUID
    academic_year_id: uuid.UUID
    level_id: uuid.UUID
    name: str
    status: str = "active"


class CurriculumRead(TimestampRead):
    establishment_id: uuid.UUID
    academic_year_id: uuid.UUID
    level_id: uuid.UUID
    name: str
    status: str

class CurriculumUpdate(BaseModel):
    academic_year_id: uuid.UUID | None = None
    level_id: uuid.UUID | None = None
    name: str | None = None
    status: str | None = None


class SubjectCreate(BaseModel):
    name: str
    code: str


class SubjectRead(TimestampRead):
    name: str
    code: str

class SubjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class CurriculumSubjectCreate(BaseModel):
    coefficient: int = 1
    weekly_hours: int


class CurriculumSubjectRead(TimestampRead):
    curriculum_id: uuid.UUID
    subject_id: uuid.UUID
    coefficient: int
    weekly_hours: int


class ClassCurriculumCreate(BaseModel):
    class_id: uuid.UUID
    curriculum_id: uuid.UUID


class ClassCurriculumRead(TimestampRead):
    class_id: uuid.UUID
    curriculum_id: uuid.UUID


class TeacherAssignmentCreate(BaseModel):
    user_id: uuid.UUID
    class_id: uuid.UUID
    curriculum_subject_id: uuid.UUID


class TeacherAssignmentRead(TimestampRead):
    user_id: uuid.UUID
    class_id: uuid.UUID
    curriculum_subject_id: uuid.UUID