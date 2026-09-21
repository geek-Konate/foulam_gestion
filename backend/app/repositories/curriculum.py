import uuid

from sqlalchemy import select

from app.models.curriculum import ClassCurriculum, Curriculum, CurriculumSubject, Subject, TeacherAssignment
from app.repositories.base import BaseRepository


class CurriculumRepository(BaseRepository[Curriculum]):
    model = Curriculum

    async def get_by_level_and_year(
            self,
            establishment_id: uuid.UUID,
            level_id: uuid.UUID,
            academic_year_id: uuid.UUID,
    ) -> Curriculum | None:
        stmt = select(Curriculum).where(
            Curriculum.establishment_id == establishment_id,
            Curriculum.level_id == level_id,
            Curriculum.academic_year_id == academic_year_id,
            Curriculum.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_establishment(self, establishment_id):
        stmt = (
            select(Curriculum)
            .where(
                Curriculum.establishment_id == establishment_id,
                Curriculum.deleted_at.is_(None),
            )
            .order_by(Curriculum.name.asc())
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_name(self, establishment_id, name):
        stmt = select(Curriculum).where(
            Curriculum.establishment_id == establishment_id,
            Curriculum.name == name,
            Curriculum.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class SubjectRepository(BaseRepository[Subject]):
    model = Subject

    async def get_by_code(self, code: str) -> Subject | None:
        stmt = select(Subject).where(Subject.code == code)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str):
        stmt = select(Subject).where(
            Subject.name == name,
            Subject.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
class CurriculumSubjectRepository(BaseRepository[CurriculumSubject]):
    model = CurriculumSubject

    async def get_by_curriculum(self, curriculum_id: uuid.UUID) -> list[CurriculumSubject]:
        stmt = select(CurriculumSubject).where(
            CurriculumSubject.curriculum_id == curriculum_id, CurriculumSubject.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class ClassCurriculumRepository(BaseRepository[ClassCurriculum]):
    model = ClassCurriculum

    async def get_by_class(self, class_id: uuid.UUID) -> ClassCurriculum | None:
        stmt = select(ClassCurriculum).where(
            ClassCurriculum.class_id == class_id, ClassCurriculum.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class TeacherAssignmentRepository(BaseRepository[TeacherAssignment]):
    model = TeacherAssignment

    async def get_by_teacher(self, user_id: uuid.UUID) -> list[TeacherAssignment]:
        stmt = select(TeacherAssignment).where(
            TeacherAssignment.user_id == user_id, TeacherAssignment.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_class(self, class_id: uuid.UUID) -> list[TeacherAssignment]:
        stmt = select(TeacherAssignment).where(
            TeacherAssignment.class_id == class_id, TeacherAssignment.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())