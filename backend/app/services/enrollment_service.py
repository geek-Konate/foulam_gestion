from uuid import UUID

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.student import (
    AcademicYearRepository,
    ClassRepository,
    EnrollmentRepository,
    StudentRepository,
)
from app.schemas.student import EnrollmentCreate, EnrollmentUpdate


class EnrollmentService:
    def __init__(
        self,
        enrollment_repo: EnrollmentRepository,
        student_repo: StudentRepository,
        class_repo: ClassRepository,
        academic_year_repo: AcademicYearRepository,
    ):
        self.enrollment_repo = enrollment_repo
        self.student_repo = student_repo
        self.class_repo = class_repo
        self.academic_year_repo = academic_year_repo

    async def _get_student(
        self,
        establishment_id: UUID,
        student_id: UUID,
    ):
        student = await self.student_repo.get(student_id)

        if not student:
            raise NotFoundException("Élève introuvable")

        if student.establishment_id != establishment_id:
            raise NotFoundException("Élève introuvable")

        return student

    async def _get_class(
        self,
        establishment_id: UUID,
        class_id: UUID,
    ):
        school_class = await self.class_repo.get(class_id)

        if not school_class:
            raise NotFoundException("Classe introuvable")

        academic_year = await self.academic_year_repo.get(
            school_class.academic_year_id
        )

        if not academic_year:
            raise NotFoundException("Classe introuvable")

        if academic_year.establishment_id != establishment_id:
            raise NotFoundException("Classe introuvable")

        return school_class

    async def create_enrollment(
        self,
        establishment_id: UUID,
        data: EnrollmentCreate,
    ):
        await self._get_student(
            establishment_id,
            data.student_id,
        )

        school_class = await self._get_class(
            establishment_id,
            data.class_id,
        )

        existing = await self.enrollment_repo.get_by_student_and_class(
            data.student_id,
            data.class_id,
        )

        if existing:
            raise ConflictException(
                "Cet élève est déjà inscrit dans cette classe"
            )

        current_enrollment = await self.enrollment_repo.get_active_by_student(
            data.student_id
        )

        if current_enrollment:
            raise ConflictException(
                "Cet élève possède déjà une inscription active"
            )

        return await self.enrollment_repo.create(
            data.model_dump()
        )

    async def list_enrollments(
        self,
        establishment_id: UUID,
        student_id: UUID | None = None,
    ):
        if student_id:
            await self._get_student(
                establishment_id,
                student_id,
            )

            return await self.enrollment_repo.get_by_student(
                student_id
            )

        return await self.enrollment_repo.get_by_establishment(
            establishment_id
        )

    async def get_enrollment(
        self,
        establishment_id: UUID,
        enrollment_id: UUID,
    ):
        enrollment = await self.enrollment_repo.get(
            enrollment_id
        )

        if not enrollment:
            raise NotFoundException(
                "Inscription introuvable"
            )

        await self._get_student(
            establishment_id,
            enrollment.student_id,
        )

        return enrollment

    async def update_enrollment(
        self,
        establishment_id: UUID,
        enrollment_id: UUID,
        data: EnrollmentUpdate,
    ):
        enrollment = await self.get_enrollment(
            establishment_id,
            enrollment_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "class_id" in update_data:
            await self._get_class(
                establishment_id,
                update_data["class_id"],
            )

            existing = (
                await self.enrollment_repo
                .get_by_student_and_class(
                    enrollment.student_id,
                    update_data["class_id"],
                )
            )

            if existing and existing.id != enrollment.id:
                raise ConflictException(
                    "Cet élève est déjà inscrit dans cette classe"
                )

        return await self.enrollment_repo.update(
            enrollment,
            update_data,
        )

    async def delete_enrollment(
        self,
        establishment_id: UUID,
        enrollment_id: UUID,
    ):
        enrollment = await self.get_enrollment(
            establishment_id,
            enrollment_id,
        )

        return await self.enrollment_repo.soft_delete(
            enrollment
        )