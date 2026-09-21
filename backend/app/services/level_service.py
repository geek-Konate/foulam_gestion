from uuid import UUID

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.student import LevelRepository
from app.schemas.student import LevelCreate, LevelUpdate


class LevelService:
    def __init__(self, level_repo: LevelRepository):
        self.level_repo = level_repo

    async def create_level(self, data: LevelCreate):
        levels = await self.level_repo.list()

        for level in levels:
            if level.name.lower() == data.name.lower():
                raise ConflictException(
                    "Un niveau avec ce nom existe déjà"
                )

        return await self.level_repo.create(
            data.model_dump()
        )

    async def list_levels(self):
        return await self.level_repo.list()

    async def get_level(self, level_id: UUID):
        level = await self.level_repo.get(level_id)

        if not level:
            raise NotFoundException("Niveau introuvable")

        return level

    async def update_level(
        self,
        level_id: UUID,
        data: LevelUpdate,
    ):
        level = await self.get_level(level_id)

        update_data = data.model_dump(exclude_unset=True)

        if "name" in update_data:
            levels = await self.level_repo.list()

            for existing_level in levels:
                if (
                    existing_level.id != level.id
                    and existing_level.name.lower()
                    == update_data["name"].lower()
                ):
                    raise ConflictException(
                        "Un niveau avec ce nom existe déjà"
                    )

        return await self.level_repo.update(
            level,
            update_data,
        )

    async def delete_level(self, level_id: UUID):
        level = await self.get_level(level_id)

        return await self.level_repo.soft_delete(level)