import uuid
from datetime import datetime, timezone

from sqlalchemy import select

from app.core.exceptions import ConflictException, NotFoundException

from app.models.student import Class
from app.repositories.academic import ReportCardRepository
from app.repositories.student import (
    StudentRepository,
    EnrollmentRepository,
    AcademicYearRepository,
)
from app.schemas.academic import ReportCardCreate


class ReportCardService:

    def __init__(
        self,
        report_card_repo: ReportCardRepository,
        student_repo: StudentRepository,
        enrollment_repo: EnrollmentRepository,
        academic_year_repo: AcademicYearRepository,
    ):
        self.report_card_repo = report_card_repo
        self.student_repo = student_repo
        self.enrollment_repo = enrollment_repo
        self.academic_year_repo = academic_year_repo

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

    async def _get_academic_year(
        self,
        establishment_id: uuid.UUID,
        academic_year_id: uuid.UUID,
    ):
        academic_year = await self.academic_year_repo.get(
            academic_year_id
        )

        if not academic_year:
            raise NotFoundException("Année scolaire introuvable")

        if academic_year.establishment_id != establishment_id:
            raise NotFoundException("Année scolaire introuvable")

        return academic_year

    async def _validate_student_enrollment(
        self,
        student_id: uuid.UUID,
        academic_year_id: uuid.UUID,
    ):
        enrollment = await self.enrollment_repo.get_active_enrollment(
            student_id
        )

        if not enrollment:
            raise NotFoundException(
                "L'élève n'a pas d'inscription active"
            )

        # Récupérer la classe explicitement (éviter MissingGreenlet)
        stmt = select(Class.academic_year_id).where(
            Class.id == enrollment.class_id,
            Class.deleted_at.is_(None),
        )
        result = await self.enrollment_repo.session.execute(stmt)
        row = result.scalar_one_or_none()

        if row  and row == academic_year_id:
            return enrollment

        raise NotFoundException(
            "L'élève n'est pas inscrit pour cette année scolaire"
        )

    async def generate(
            self,
            establishment_id: uuid.UUID,
            data: ReportCardCreate,
    ):
        await self._get_student(
            establishment_id,
            data.student_id,
        )

        await self._get_academic_year(
            establishment_id,
            data.academic_year_id,
        )

        await self._validate_student_enrollment(
            data.student_id,
            data.academic_year_id,
        )

        existing = await self.report_card_repo.get_by_student_year_and_period(
            data.student_id,
            data.academic_year_id,
            data.period,
        )

        if existing:
            raise ConflictException(
                "Un bulletin existe déjà pour cet élève, "
                "cette année scolaire et cette période"
            )

        return await self.report_card_repo.create(
            data.model_dump()
        )

    async def get(
        self,
        establishment_id: uuid.UUID,
        report_card_id: uuid.UUID,
    ):
        report_card = await self.report_card_repo.get(
            report_card_id
        )

        if not report_card:
            raise NotFoundException("Bulletin introuvable")

        await self._get_student(
            establishment_id,
            report_card.student_id,
        )

        return report_card

    async def list_by_student(
        self,
        establishment_id: uuid.UUID,
        student_id: uuid.UUID,
        academic_year_id: uuid.UUID | None = None,
    ):
        await self._get_student(
            establishment_id,
            student_id,
        )

        if academic_year_id is not None:
            await self._get_academic_year(
                establishment_id,
                academic_year_id,
            )

            return await self.report_card_repo.get_by_student_and_year(
                student_id,
                academic_year_id,
            )

        return await self.report_card_repo.get_by_student(
            student_id,
        )