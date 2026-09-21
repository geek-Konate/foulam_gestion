import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.curriculum import CurriculumRepository
from app.repositories.student import AcademicYearRepository
from app.repositories.student import LevelRepository


class CurriculumService:

    def __init__(
        self,
        curriculum_repo: CurriculumRepository,
        academic_year_repo: AcademicYearRepository,
        level_repo: LevelRepository,
    ):
        self.curriculum_repo = curriculum_repo
        self.academic_year_repo = academic_year_repo
        self.level_repo = level_repo

    async def _validate_academic_year(
        self,
        establishment_id: uuid.UUID,
        academic_year_id: uuid.UUID,
    ):
        academic_year = await self.academic_year_repo.get(academic_year_id)

        if not academic_year:
            raise NotFoundException("Année scolaire introuvable")

        if academic_year.establishment_id != establishment_id:
            raise NotFoundException("Année scolaire introuvable")

        return academic_year

    async def _validate_level(
        self,
        level_id: uuid.UUID,
    ):
        level = await self.level_repo.get(level_id)

        if not level:
            raise NotFoundException("Niveau introuvable")

        return level

    async def create_curriculum(
        self,
        establishment_id: uuid.UUID,
        data,
    ):
        # Vérification de l'année scolaire
        await self._validate_academic_year(
            establishment_id,
            data.academic_year_id,
        )

        # Vérification du niveau
        await self._validate_level(data.level_id)

        # Une seule maquette pour un niveau donné dans une année
        existing = await self.curriculum_repo.get_by_level_and_year(
            establishment_id,
            data.level_id,
            data.academic_year_id,
        )

        if existing:
            raise ConflictException(
                "Une maquette existe déjà pour ce niveau et cette année scolaire"
            )

        payload = data.model_dump()

        # L'établissement utilisé dans l'URL est la source de vérité
        payload["establishment_id"] = establishment_id

        return await self.curriculum_repo.create(payload)

    async def list_curriculums(
        self,
        establishment_id: uuid.UUID,
    ):
        return await self.curriculum_repo.get_by_establishment(
            establishment_id
        )

    async def get_curriculum(
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

    async def update_curriculum(
        self,
        establishment_id: uuid.UUID,
        curriculum_id: uuid.UUID,
        data,
    ):
        curriculum = await self.get_curriculum(
            establishment_id,
            curriculum_id,
        )

        new_academic_year_id = (
            data.academic_year_id
            if data.academic_year_id is not None
            else curriculum.academic_year_id
        )

        new_level_id = (
            data.level_id
            if data.level_id is not None
            else curriculum.level_id
        )

        # Vérifier l'année scolaire
        await self._validate_academic_year(
            establishment_id,
            new_academic_year_id,
        )

        # Vérifier le niveau
        await self._validate_level(new_level_id)

        # Vérifier qu'on ne crée pas un doublon
        existing = await self.curriculum_repo.get_by_level_and_year(
            establishment_id,
            new_level_id,
            new_academic_year_id,
        )

        if existing and existing.id != curriculum.id:
            raise ConflictException(
                "Une maquette existe déjà pour ce niveau et cette année scolaire"
            )

        payload = data.model_dump(exclude_unset=True)

        return await self.curriculum_repo.update(
            curriculum,
            payload,
        )

    async def delete_curriculum(
        self,
        establishment_id: uuid.UUID,
        curriculum_id: uuid.UUID,
    ):
        curriculum = await self.get_curriculum(
            establishment_id,
            curriculum_id,
        )

        return await self.curriculum_repo.soft_delete(curriculum)