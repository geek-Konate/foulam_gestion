import uuid
from datetime import date

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.academic import AttendanceRepository
from app.repositories.student import (
    StudentRepository,
    EnrollmentRepository,
    ClassRepository,
    AcademicYearRepository,
)


class AttendanceService:

    def __init__(
        self,
        attendance_repo: AttendanceRepository,
        student_repo: StudentRepository,
        enrollment_repo: EnrollmentRepository,
        class_repo: ClassRepository,
        academic_year_repo: AcademicYearRepository,
    ):
        self.attendance_repo = attendance_repo
        self.student_repo = student_repo
        self.enrollment_repo = enrollment_repo
        self.class_repo = class_repo
        self.academic_year_repo = academic_year_repo

    async def _get_class(
        self,
        establishment_id: uuid.UUID,
        class_id: uuid.UUID,
    ):
        school_class = await self.class_repo.get(class_id)

        if not school_class:
            raise NotFoundException("Classe introuvable")

        academic_year = await self.academic_year_repo.get(
            school_class.academic_year_id
        )

        if not academic_year:
            raise NotFoundException(
                "Année scolaire introuvable"
            )

        if academic_year.establishment_id != establishment_id:
            raise NotFoundException("Classe introuvable")

        return school_class

    async def _get_student(
        self,
        establishment_id: uuid.UUID,
        student_id: uuid.UUID,
    ):
        student = await self.student_repo.get(student_id)

        if not student:
            raise NotFoundException("Élève introuvable")

        if student.establishment_id != establishment_id:
            raise NotFoundException("Élève introuvable")

        return student

    async def _validate_student_in_class(
        self,
        student_id: uuid.UUID,
        class_id: uuid.UUID,
    ):
        enrollments = await self.enrollment_repo.get_by_student(
            student_id
        )

        for enrollment in enrollments:
            if (
                enrollment.class_id == class_id
                and enrollment.status == "active"
            ):
                return enrollment

        raise ConflictException(
            "Cet élève n'est pas inscrit dans cette classe"
        )

    async def create_attendance(
        self,
        establishment_id: uuid.UUID,
        data,
    ):
        await self._get_class(
            establishment_id,
            data.class_id,
        )

        await self._get_student(
            establishment_id,
            data.student_id,
        )

        await self._validate_student_in_class(
            data.student_id,
            data.class_id,
        )

        existing = await self.attendance_repo.get_by_class_and_date(
            data.class_id,
            data.date,
        )

        for attendance in existing:
            if attendance.student_id == data.student_id:
                raise ConflictException(
                    "Une présence existe déjà pour cet élève à cette date"
                )

        return await self.attendance_repo.create(
            data.model_dump()
        )

    async def list_by_class_and_date(
        self,
        establishment_id: uuid.UUID,
        class_id: uuid.UUID,
        attendance_date: date,
    ):
        await self._get_class(
            establishment_id,
            class_id,
        )

        return await self.attendance_repo.get_by_class_and_date(
            class_id,
            attendance_date,
        )

    async def list_by_student(
        self,
        establishment_id: uuid.UUID,
        student_id: uuid.UUID,
    ):
        await self._get_student(
            establishment_id,
            student_id,
        )

        return await self.attendance_repo.get_by_student(
            student_id
        )

    async def get_attendance(
        self,
        establishment_id: uuid.UUID,
        attendance_id: uuid.UUID,
    ):
        attendance = await self.attendance_repo.get(
            attendance_id
        )

        if not attendance:
            raise NotFoundException(
                "Enregistrement de présence introuvable"
            )

        await self._get_class(
            establishment_id,
            attendance.class_id,
        )

        return attendance

    async def update_attendance(
        self,
        establishment_id: uuid.UUID,
        attendance_id: uuid.UUID,
        data,
    ):
        attendance = await self.get_attendance(
            establishment_id,
            attendance_id,
        )

        payload = data.model_dump(
            exclude_unset=True
        )

        return await self.attendance_repo.update(
            attendance,
            payload,
        )

    async def delete_attendance(
        self,
        establishment_id: uuid.UUID,
        attendance_id: uuid.UUID,
    ):
        attendance = await self.get_attendance(
            establishment_id,
            attendance_id,
        )

        return await self.attendance_repo.soft_delete(
            attendance
        )