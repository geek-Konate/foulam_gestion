import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.student import AcademicYearRepository
from app.schemas.student import AcademicYearCreate, AcademicYearUpdate


class AcademicYearService:
    def __init__(self, academic_year_repo: AcademicYearRepository):
        self.academic_year_repo = academic_year_repo

    async def create_academic_year(
        self,
        establishment_id: uuid.UUID,
        data: AcademicYearCreate,
    ):
        if data.start_date >= data.end_date:
            raise ConflictException(
                "La date de début doit être antérieure à la date de fin"
            )

        existing = await self.academic_year_repo.get_by_name(
            establishment_id=establishment_id,
            name=data.name,
        )

        if existing:
            raise ConflictException(
                "Cette année académique existe déjà dans cet établissement"
            )

        if data.status == "active":
            active_year = await self.academic_year_repo.get_current(
                establishment_id
            )

            if active_year:
                raise ConflictException(
                    "Cet établissement possède déjà une année académique active"
                )

        return await self.academic_year_repo.create(
            {
                "establishment_id": establishment_id,
                "name": data.name,
                "start_date": data.start_date,
                "end_date": data.end_date,
                "status": data.status,
            }
        )

    async def list_academic_years(
        self,
        establishment_id: uuid.UUID,
    ):
        return await self.academic_year_repo.get_by_establishment(
            establishment_id
        )

    async def get_academic_year(
        self,
        establishment_id: uuid.UUID,
        academic_year_id: uuid.UUID,
    ):
        academic_year = await self.academic_year_repo.get(
            academic_year_id
        )

        if not academic_year:
            raise NotFoundException(
                "Année académique introuvable"
            )

        if academic_year.establishment_id != establishment_id:
            raise ConflictException(
                "Cette année académique n'appartient pas à cet établissement"
            )

        return academic_year

    async def update_academic_year(
        self,
        establishment_id: uuid.UUID,
        academic_year_id: uuid.UUID,
        data: AcademicYearUpdate,
    ):
        academic_year = await self.get_academic_year(
            establishment_id=establishment_id,
            academic_year_id=academic_year_id,
        )

        update_data = data.model_dump(exclude_unset=True)

        start_date = update_data.get(
            "start_date",
            academic_year.start_date,
        )

        end_date = update_data.get(
            "end_date",
            academic_year.end_date,
        )

        if start_date >= end_date:
            raise ConflictException(
                "La date de début doit être antérieure à la date de fin"
            )

        if update_data.get("status") == "active":
            active_year = await self.academic_year_repo.get_current(
                establishment_id
            )

            if active_year and active_year.id != academic_year.id:
                raise ConflictException(
                    "Cet établissement possède déjà une année académique active"
                )

        if "name" in update_data:
            existing = await self.academic_year_repo.get_by_name(
                establishment_id=establishment_id,
                name=update_data["name"],
            )

            if existing and existing.id != academic_year.id:
                raise ConflictException(
                    "Cette année académique existe déjà dans cet établissement"
                )

        return await self.academic_year_repo.update(
            academic_year,
            update_data,
        )

    async def delete_academic_year(
        self,
        establishment_id: uuid.UUID,
        academic_year_id: uuid.UUID,
    ):
        academic_year = await self.get_academic_year(
            establishment_id=establishment_id,
            academic_year_id=academic_year_id,
        )

        if academic_year.status == "active":
            raise ConflictException(
                "Une année académique active ne peut pas être supprimée"
            )

        return await self.academic_year_repo.soft_delete(
            academic_year
        )