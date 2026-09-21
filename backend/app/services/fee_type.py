import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.finance import FeeTypeRepository


class FeeTypeService:

    def __init__(
        self,
        fee_type_repo: FeeTypeRepository,
    ):
        self.fee_type_repo = fee_type_repo

    async def create(
        self,
        establishment_id: uuid.UUID,
        data,
    ):
        if data.amount <= 0:
            raise ConflictException(
                "Le montant du frais doit être supérieur à zéro"
            )

        existing = await self.fee_type_repo.get_by_name(
            establishment_id=establishment_id,
            name=data.name,
        )

        if existing:
            raise ConflictException(
                "Ce type de frais existe déjà dans cet établissement"
            )

        return await self.fee_type_repo.create(
            {
                "establishment_id": establishment_id,
                "name": data.name,
                "amount": data.amount,
            }
        )

    async def list(
        self,
        establishment_id: uuid.UUID,
    ):
        return await self.fee_type_repo.get_by_establishment(
            establishment_id
        )

    async def get(
        self,
        establishment_id: uuid.UUID,
        fee_type_id: uuid.UUID,
    ):
        fee_type = await self.fee_type_repo.get(fee_type_id)

        if not fee_type:
            raise NotFoundException(
                "Type de frais introuvable"
            )

        if fee_type.establishment_id != establishment_id:
            raise NotFoundException(
                "Type de frais introuvable"
            )

        return fee_type

    async def update(
        self,
        establishment_id: uuid.UUID,
        fee_type_id: uuid.UUID,
        data,
    ):
        fee_type = await self.get(
            establishment_id,
            fee_type_id,
        )

        if data.amount <= 0:
            raise ConflictException(
                "Le montant du frais doit être supérieur à zéro"
            )

        if data.name != fee_type.name:
            existing = await self.fee_type_repo.get_by_name(
                establishment_id=establishment_id,
                name=data.name,
            )

            if existing and existing.id != fee_type_id:
                raise ConflictException(
                    "Ce type de frais existe déjà dans cet établissement"
                )

        return await self.fee_type_repo.update(
            fee_type,
            {
                "name": data.name,
                "amount": data.amount,
            },
        )

    async def delete(
        self,
        establishment_id: uuid.UUID,
        fee_type_id: uuid.UUID,
    ):
        fee_type = await self.get(
            establishment_id,
            fee_type_id,
        )

        return await self.fee_type_repo.soft_delete(
            fee_type
        )