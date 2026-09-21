import uuid
from datetime import date

from pydantic import BaseModel, EmailStr, ConfigDict

from app.schemas.base import TimestampRead


class AcademicYearCreate(BaseModel):
    name: str
    start_date: date
    end_date: date
    status: str = "active"


class AcademicYearRead(TimestampRead):
    establishment_id: uuid.UUID
    name: str
    start_date: date
    end_date: date
    status: str

class AcademicYearUpdate(BaseModel):
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None

class LevelCreate(BaseModel):
    name: str
    category: str


class LevelUpdate(BaseModel):
    name: str | None = None
    category: str | None = None


class LevelRead(TimestampRead):
    name: str
    category: str


class ClassCreate(BaseModel):
    academic_year_id: uuid.UUID
    level_id: uuid.UUID
    name: str
    capacity: int = 30


class ClassUpdate(BaseModel):
    name: str | None = None
    capacity: int | None = None


class ClassRead(TimestampRead):
    academic_year_id: uuid.UUID
    level_id: uuid.UUID
    name: str
    capacity: int


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    photo: str | None = None


class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    photo: str | None = None


class StudentRead(TimestampRead):
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    photo: str | None


class GuardianCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class GuardianUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class GuardianRead(TimestampRead):
    establishment_id: uuid.UUID
    first_name: str
    last_name: str
    phone: str | None
    email: EmailStr | None
    address: str | None

    model_config = ConfigDict(from_attributes=True)


class StudentGuardianCreate(BaseModel):
    student_id: uuid.UUID
    guardian_id: uuid.UUID
    relationship_type: str


class StudentGuardianRead(TimestampRead):
    student_id: uuid.UUID
    guardian_id: uuid.UUID
    relationship_type: str


class EnrollmentCreate(BaseModel):
    student_id: uuid.UUID
    class_id: uuid.UUID
    enrollment_date: date
    status: str = "active"


class EnrollmentUpdate(BaseModel):
    status: str | None = None


class EnrollmentRead(TimestampRead):
    student_id: uuid.UUID
    class_id: uuid.UUID
    enrollment_date: date
    status: str