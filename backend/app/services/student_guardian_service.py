from uuid import UUID

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.student import (
    GuardianRepository,
    StudentGuardianRepository,
    StudentRepository,
)
from app.schemas.student import StudentGuardianCreate


class StudentGuardianService:
    def __init__(
        self,
        student_guardian_repo: StudentGuardianRepository,
        student_repo: StudentRepository,
        guardian_repo: GuardianRepository,
    ):
        self.student_guardian_repo = student_guardian_repo
        self.student_repo = student_repo
        self.guardian_repo = guardian_repo

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

    async def _get_guardian(
        self,
        establishment_id: UUID,
        guardian_id: UUID,
    ):
        guardian = await self.guardian_repo.get(guardian_id)

        if not guardian:
            raise NotFoundException("Responsable introuvable")

        if guardian.establishment_id != establishment_id:
            raise NotFoundException("Responsable introuvable")

        return guardian

    async def create_link(
        self,
        establishment_id: UUID,
        student_id: UUID,
        data: StudentGuardianCreate,
    ):
        await self._get_student(
            establishment_id,
            student_id,
        )

        await self._get_guardian(
            establishment_id,
            data.guardian_id,
        )

        existing = await self.student_guardian_repo.get_link(
            student_id,
            data.guardian_id,
        )

        if existing:
            raise ConflictException(
                "Ce responsable est déjà associé à cet élève"
            )

        return await self.student_guardian_repo.create(
            {
                "student_id": student_id,
                "guardian_id": data.guardian_id,
                "relationship_type": data.relationship_type,
            }
        )

    async def list_guardians(
        self,
        establishment_id: UUID,
        student_id: UUID,
    ):
        await self._get_student(
            establishment_id,
            student_id,
        )

        return await self.student_guardian_repo.get_guardians_for_student(
            student_id
        )

    async def delete_link(
        self,
        establishment_id: UUID,
        student_id: UUID,
        guardian_id: UUID,
    ):
        await self._get_student(
            establishment_id,
            student_id,
        )

        await self._get_guardian(
            establishment_id,
            guardian_id,
        )

        link = await self.student_guardian_repo.get_link(
            student_id,
            guardian_id,
        )

        if not link:
            raise NotFoundException(
                "Association introuvable"
            )

        return await self.student_guardian_repo.soft_delete(
            link
        )