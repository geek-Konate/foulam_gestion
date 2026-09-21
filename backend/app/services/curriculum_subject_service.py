import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.curriculum import (
    CurriculumRepository,
    CurriculumSubjectRepository,
    SubjectRepository,
)


class CurriculumSubjectService:

    def __init__(
        self,
        curriculum_subject_repo: CurriculumSubjectRepository,
        curriculum_repo: CurriculumRepository,
        subject_repo: SubjectRepository,
    ):
        self.curriculum_subject_repo = curriculum_subject_repo
        self.curriculum_repo = curriculum_repo
        self.subject_repo = subject_repo

    async def _get_curriculum(
        self,
        establishment_id: uuid.UUID,
        curriculum_id: uuid.UUID,
    ):
        curriculum = await self.curriculum_repo.get(curriculum_id)

        if not curriculum:
            raise NotFoundException("Maquette introuvable")

        if curriculum.establishment_id != establishment_id:
            raise NotFoundException("Maquette introuvable")

        return curriculum

    async def _get_subject(
        self,
        subject_id: uuid.UUID,
    ):
        subject = await self.subject_repo.get(subject_id)

        if not subject:
            raise NotFoundException("Matière introuvable")

        return subject

    async def list_subjects(
        self,
        establishment_id: uuid.UUID,
        curriculum_id: uuid.UUID,
    ):
        await self._get_curriculum(
            establishment_id,
            curriculum_id,
        )

        return await self.curriculum_subject_repo.get_by_curriculum(
            curriculum_id
        )

    async def add_subject(
        self,
        establishment_id: uuid.UUID,
        curriculum_id: uuid.UUID,
        subject_id: uuid.UUID,
        data,
    ):
        await self._get_curriculum(
            establishment_id,
            curriculum_id,
        )

        await self._get_subject(subject_id)

        if data.coefficient <= 0:
            raise ConflictException(
                "Le coefficient doit être supérieur à 0"
            )

        if data.weekly_hours <= 0:
            raise ConflictException(
                "Le nombre d'heures hebdomadaires doit être supérieur à 0"
            )

        existing_subjects = (
            await self.curriculum_subject_repo.get_by_curriculum(
                curriculum_id
            )
        )

        for item in existing_subjects:
            if item.subject_id == subject_id:
                raise ConflictException(
                    "Cette matière est déjà associée à cette maquette"
                )

        payload = data.model_dump()

        # Les IDs de la route sont les valeurs de référence
        payload["curriculum_id"] = curriculum_id
        payload["subject_id"] = subject_id

        return await self.curriculum_subject_repo.create(payload)

    async def remove_subject(
        self,
        establishment_id: uuid.UUID,
        curriculum_id: uuid.UUID,
        subject_id: uuid.UUID,
    ):
        await self._get_curriculum(
            establishment_id,
            curriculum_id,
        )

        subjects = await self.curriculum_subject_repo.get_by_curriculum(
            curriculum_id
        )

        curriculum_subject = next(
            (
                item
                for item in subjects
                if item.subject_id == subject_id
            ),
            None,
        )

        if not curriculum_subject:
            raise NotFoundException(
                "Cette matière n'est pas associée à cette maquette"
            )

        return await self.curriculum_subject_repo.soft_delete(
            curriculum_subject
        )