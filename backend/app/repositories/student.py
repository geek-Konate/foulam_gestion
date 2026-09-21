import uuid

from sqlalchemy import select

from app.models.student import AcademicYear, Class, Enrollment, Guardian, Level, Student, StudentGuardian
from app.repositories.base import BaseRepository


class AcademicYearRepository(BaseRepository[AcademicYear]):
    model = AcademicYear

    async def get_current(
        self,
        establishment_id: uuid.UUID,
    ) -> AcademicYear | None:
        stmt = select(AcademicYear).where(
            AcademicYear.establishment_id == establishment_id,
            AcademicYear.status == "active",
            AcademicYear.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        establishment_id: uuid.UUID,
        name: str,
    ) -> AcademicYear | None:
        stmt = select(AcademicYear).where(
            AcademicYear.establishment_id == establishment_id,
            AcademicYear.name == name,
            AcademicYear.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_establishment(
        self,
        establishment_id: uuid.UUID,
    ) -> list[AcademicYear]:
        stmt = (
            select(AcademicYear)
            .where(
                AcademicYear.establishment_id == establishment_id,
                AcademicYear.deleted_at.is_(None),
            )
            .order_by(AcademicYear.start_date.desc())
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

class LevelRepository(BaseRepository[Level]):
    model = Level


class ClassRepository(BaseRepository[Class]):
    model = Class

    async def get_by_academic_year(self, academic_year_id: uuid.UUID) -> list[Class]:
        stmt = select(Class).where(
            Class.academic_year_id == academic_year_id, Class.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class StudentRepository(BaseRepository[Student]):
    model = Student

    async def search_by_name(self, query: str) -> list[Student]:
        pattern = f"%{query}%"
        stmt = select(Student).where(
            (Student.first_name.ilike(pattern)) | (Student.last_name.ilike(pattern)),
            Student.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class GuardianRepository(BaseRepository[Guardian]):
    model = Guardian

    async def get_by_establishment(self, establishment_id: uuid.UUID):
        stmt = select(Guardian).where(
            Guardian.establishment_id == establishment_id,
            Guardian.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_by_email(self, email: str):
        stmt = select(Guardian).where(
            Guardian.email == email,
            Guardian.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()



class StudentGuardianRepository(BaseRepository[StudentGuardian]):
    model = StudentGuardian

    async def get_guardians_for_student(self, student_id: uuid.UUID) -> list[StudentGuardian]:
        stmt = select(StudentGuardian).where(
            StudentGuardian.student_id == student_id, StudentGuardian.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_link(
            self,
            student_id: uuid.UUID,
            guardian_id: uuid.UUID,
    ):
        stmt = select(StudentGuardian).where(
            StudentGuardian.student_id == student_id,
            StudentGuardian.guardian_id == guardian_id,
            StudentGuardian.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()


class EnrollmentRepository(BaseRepository[Enrollment]):
    model = Enrollment

    async def get_history_for_student(self, student_id: uuid.UUID) -> list[Enrollment]:
        stmt = (
            select(Enrollment)
            .where(Enrollment.student_id == student_id)
            .order_by(Enrollment.enrollment_date.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_active_enrollment(self, student_id: uuid.UUID) -> Enrollment | None:
        stmt = select(Enrollment).where(
            Enrollment.student_id == student_id,
            Enrollment.status == "active",
            Enrollment.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_class(self, class_id: uuid.UUID) -> list[Enrollment]:
        stmt = select(Enrollment).where(
            Enrollment.class_id == class_id,
            Enrollment.status == "active",
            Enrollment.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_student_and_class(
            self,
            student_id: uuid.UUID,
            class_id: uuid.UUID,
    ):
        stmt = select(Enrollment).where(
            Enrollment.student_id == student_id,
            Enrollment.class_id == class_id,
            Enrollment.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_active_by_student(
            self,
            student_id: uuid.UUID,
    ):
        stmt = select(Enrollment).where(
            Enrollment.student_id == student_id,
            Enrollment.status == "active",
            Enrollment.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_establishment(
            self,
            establishment_id: uuid.UUID,
    ):
        stmt = (
            select(Enrollment)
            .join(Class, Enrollment.class_id == Class.id)
            .join(
                AcademicYear,
                Class.academic_year_id == AcademicYear.id,
            )
            .where(
                AcademicYear.establishment_id == establishment_id,
                Enrollment.deleted_at.is_(None),
            )
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()