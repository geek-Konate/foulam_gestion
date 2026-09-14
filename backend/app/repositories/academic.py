import uuid

from sqlalchemy import select

from app.models.academic import Attendance, Evaluation, Grade, ReportCard
from app.repositories.base import BaseRepository


class EvaluationRepository(BaseRepository[Evaluation]):
    model = Evaluation

    async def get_by_class_and_period(self, class_id: uuid.UUID, period: str) -> list[Evaluation]:
        stmt = select(Evaluation).where(
            Evaluation.class_id == class_id, Evaluation.period == period, Evaluation.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class GradeRepository(BaseRepository[Grade]):
    model = Grade

    async def get_by_evaluation(self, evaluation_id: uuid.UUID) -> list[Grade]:
        stmt = select(Grade).where(
            Grade.evaluation_id == evaluation_id, Grade.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_student(self, student_id: uuid.UUID) -> list[Grade]:
        stmt = select(Grade).where(Grade.student_id == student_id, Grade.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class AttendanceRepository(BaseRepository[Attendance]):
    model = Attendance

    async def get_by_class_and_date(self, class_id: uuid.UUID, date) -> list[Attendance]:
        stmt = select(Attendance).where(
            Attendance.class_id == class_id, Attendance.date == date, Attendance.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_student(self, student_id: uuid.UUID) -> list[Attendance]:
        stmt = select(Attendance).where(
            Attendance.student_id == student_id, Attendance.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class ReportCardRepository(BaseRepository[ReportCard]):
    model = ReportCard

    async def get_by_student_and_year(
        self, student_id: uuid.UUID, academic_year_id: uuid.UUID
    ) -> list[ReportCard]:
        stmt = select(ReportCard).where(
            ReportCard.student_id == student_id,
            ReportCard.academic_year_id == academic_year_id,
            ReportCard.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())