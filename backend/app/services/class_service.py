from uuid import UUID

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.student import (
    AcademicYearRepository,
    ClassRepository,
    LevelRepository,
)
from app.schemas.student import ClassCreate, ClassUpdate


class ClassService:
    def __init__(
        self,
        class_repo: ClassRepository,
        academic_year_repo: AcademicYearRepository,
        level_repo: LevelRepository,
    ):
        self.class_repo = class_repo
        self.academic_year_repo = academic_year_repo
        self.level_repo = level_repo

    async def _get_academic_year(
        self,
        establishment_id: UUID,
        academic_year_id: UUID,
    ):
        academic_year = await self.academic_year_repo.get(
            academic_year_id
        )

        if not academic_year:
            raise NotFoundException(
                "Année académique introuvable"
            )

        if academic_year.establishment_id != establishment_id:
            raise NotFoundException(
                "Année académique introuvable"
            )

        return academic_year

    async def _get_level(self, level_id: UUID):
        level = await self.level_repo.get(level_id)

        if not level:
            raise NotFoundException(
                "Niveau introuvable"
            )

        return level

    async def create_class(
        self,
        establishment_id: UUID,
        data: ClassCreate,
    ):
        await self._get_academic_year(
            establishment_id,
            data.academic_year_id,
        )

        await self._get_level(data.level_id)

        existing_classes = await self.class_repo.get_by_academic_year(
            data.academic_year_id
        )

        for existing_class in existing_classes:
            if existing_class.name.lower() == data.name.lower():
                raise ConflictException(
                    "Une classe avec ce nom existe déjà dans cette année académique"
                )

        return await self.class_repo.create(
            data.model_dump()
        )

    async def list_classes(
        self,
        establishment_id: UUID,
        academic_year_id: UUID | None = None,
    ):
        if academic_year_id:
            await self._get_academic_year(
                establishment_id,
                academic_year_id,
            )

            return await self.class_repo.get_by_academic_year(
                academic_year_id
            )

        # Toutes les classes de l'établissement :
        # on récupère d'abord ses années académiques.
        academic_years = await self.academic_year_repo.get_by_establishment(
            establishment_id
        )

        classes = []

        for academic_year in academic_years:
            classes.extend(
                await self.class_repo.get_by_academic_year(
                    academic_year.id
                )
            )

        return classes

    async def get_class(
        self,
        establishment_id: UUID,
        class_id: UUID,
    ):
        school_class = await self.class_repo.get(class_id)

        if not school_class:
            raise NotFoundException(
                "Classe introuvable"
            )

        await self._get_academic_year(
            establishment_id,
            school_class.academic_year_id,
        )

        return school_class

    async def update_class(
            self,
            establishment_id: UUID,
            class_id: UUID,
            data: ClassUpdate,
    ):
        school_class = await self.get_class(
            establishment_id,
            class_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            existing_classes = (
                await self.class_repo.get_by_academic_year(
                    school_class.academic_year_id
                )
            )

            for existing_class in existing_classes:
                if (
                        existing_class.id != school_class.id
                        and existing_class.name.lower()
                        == update_data["name"].lower()
                ):
                    raise ConflictException(
                        "Une classe avec ce nom existe déjà dans cette année académique"
                    )

        return await self.class_repo.update(
            school_class,
            update_data,
        )

    async def delete_class(
        self,
        establishment_id: UUID,
        class_id: UUID,
    ):
        school_class = await self.get_class(
            establishment_id,
            class_id,
        )

        return await self.class_repo.soft_delete(
            school_class
        )