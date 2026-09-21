import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.curriculum import (
    ClassCurriculumRepository,
    CurriculumRepository,
)
from app.repositories.student import ClassRepository
from app.repositories.student import AcademicYearRepository


class ClassCurriculumService:

    def __init__(
        self,
        class_curriculum_repo: ClassCurriculumRepository,
        curriculum_repo: CurriculumRepository,
        class_repo: ClassRepository,
        academic_year_repo: AcademicYearRepository,
    ):
        self.class_curriculum_repo = class_curriculum_repo
        self.curriculum_repo = curriculum_repo
        self.class_repo = class_repo
        self.academic_year_repo = academic_year_repo

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
            raise NotFoundException("Année scolaire introuvable")

        if academic_year.establishment_id != establishment_id:
            raise NotFoundException("Classe introuvable")

        return school_class

    async def assign_curriculum(
        self,
        establishment_id: uuid.UUID,
        class_id: uuid.UUID,
        curriculum_id: uuid.UUID,
    ):
        school_class = await self._get_class(
            establishment_id,
            class_id,
        )

        curriculum = await self._get_curriculum(
            establishment_id,
            curriculum_id,
        )

        # La maquette doit correspondre à l'année scolaire de la classe
        if curriculum.academic_year_id != school_class.academic_year_id:
            raise ConflictException(
                "La maquette et la classe doivent appartenir à la même année scolaire"
            )

        # La maquette doit correspondre au niveau de la classe
        if curriculum.level_id != school_class.level_id:
            raise ConflictException(
                "La maquette et la classe doivent appartenir au même niveau"
            )

        existing = await self.class_curriculum_repo.get_by_class(
            class_id
        )

        if existing:
            if existing.curriculum_id == curriculum_id:
                raise ConflictException(
                    "Cette maquette est déjà affectée à cette classe"
                )

            raise ConflictException(
                "Une maquette est déjà affectée à cette classe"
            )

        return await self.class_curriculum_repo.create(
            {
                "class_id": class_id,
                "curriculum_id": curriculum_id,
            }
        )

    async def get_class_curriculum(
        self,
        establishment_id: uuid.UUID,
        class_id: uuid.UUID,
    ):
        await self._get_class(
            establishment_id,
            class_id,
        )

        class_curriculum = (
            await self.class_curriculum_repo.get_by_class(
                class_id
            )
        )

        if not class_curriculum:
            raise NotFoundException(
                "Aucune maquette n'est affectée à cette classe"
            )

        return class_curriculum

    async def remove_curriculum(
        self,
        establishment_id: uuid.UUID,
        class_id: uuid.UUID,
    ):
        await self._get_class(
            establishment_id,
            class_id,
        )

        class_curriculum = (
            await self.class_curriculum_repo.get_by_class(
                class_id
            )
        )

        if not class_curriculum:
            raise NotFoundException(
                "Aucune maquette n'est affectée à cette classe"
            )

        return await self.class_curriculum_repo.soft_delete(
            class_curriculum
        )