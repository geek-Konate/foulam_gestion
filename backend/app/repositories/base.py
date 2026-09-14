import uuid
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel as ORMBaseModel

ModelType = TypeVar("ModelType", bound=ORMBaseModel)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: uuid.UUID, include_deleted: bool = False) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == id)
        if not include_deleted:
            stmt = stmt.where(self.model.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
            self, skip: int = 0, limit: int = 100, include_deleted: bool = False
    ) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        if not include_deleted:
            stmt = stmt.where(self.model.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, obj_in: dict) -> ModelType:
        obj = self.model(**obj_in)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: ModelType, obj_in: dict) -> ModelType:
        for field, value in obj_in.items():
            setattr(obj, field, value)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def soft_delete(self, obj: ModelType) -> ModelType:
        from datetime import datetime, timezone

        obj.deleted_at = datetime.now(timezone.utc)

        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def hard_delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)
        await self.session.flush()

