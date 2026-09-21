from uuid import UUID

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.student import GuardianRepository
from app.schemas.student import GuardianCreate, GuardianUpdate


class GuardianService:
    def __init__(self, guardian_repo: GuardianRepository):
        self.guardian_repo = guardian_repo

    async def create_guardian(
        self,
        establishment_id: UUID,
        data: GuardianCreate,
    ):
        if data.email:
            existing = await self.guardian_repo.get_by_email(
                data.email
            )

            if existing and existing.establishment_id == establishment_id:
                raise ConflictException(
                    "Un responsable avec cet email existe déjà"
                )

        guardian_data = data.model_dump()
        guardian_data["establishment_id"] = establishment_id

        return await self.guardian_repo.create(guardian_data)

    async def list_guardians(
        self,
        establishment_id: UUID,
    ):
        return await self.guardian_repo.get_by_establishment(
            establishment_id
        )

    async def get_guardian(
        self,
        establishment_id: UUID,
        guardian_id: UUID,
    ):
        guardian = await self.guardian_repo.get(guardian_id)

        if not guardian:
            raise NotFoundException(
                "Responsable introuvable"
            )

        if guardian.establishment_id != establishment_id:
            raise NotFoundException(
                "Responsable introuvable"
            )

        return guardian

    async def update_guardian(
        self,
        establishment_id: UUID,
        guardian_id: UUID,
        data: GuardianUpdate,
    ):
        guardian = await self.get_guardian(
            establishment_id,
            guardian_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "email" in update_data and update_data["email"]:
            existing = await self.guardian_repo.get_by_email(
                update_data["email"]
            )

            if (
                existing
                and existing.id != guardian.id
                and existing.establishment_id == establishment_id
            ):
                raise ConflictException(
                    "Un responsable avec cet email existe déjà"
                )

        return await self.guardian_repo.update(
            guardian,
            update_data,
        )

    async def delete_guardian(
        self,
        establishment_id: UUID,
        guardian_id: UUID,
    ):
        guardian = await self.get_guardian(
            establishment_id,
            guardian_id,
        )

        return await self.guardian_repo.soft_delete(
            guardian
        )