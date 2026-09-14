import uuid

from sqlalchemy import select

from app.models.organization import (
    Establishment,
    Organization,
    Subscription,
)
from app.repositories.base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    model = Organization

    async def get_by_name(
        self,
        name: str,
    ) -> Organization | None:
        stmt = select(Organization).where(
            Organization.name == name,
            Organization.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        stmt = select(Organization).where(
            Organization.slug == slug,
            Organization.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class SubscriptionRepository(BaseRepository[Subscription]):
    model = Subscription

    async def get_active_by_organization(
        self,
        organization_id: uuid.UUID,
    ) -> list[Subscription]:
        stmt = select(Subscription).where(
            Subscription.organization_id == organization_id,
            Subscription.status == "active",
            Subscription.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class EstablishmentRepository(BaseRepository[Establishment]):
    model = Establishment

    async def get_by_organization(
        self,
        organization_id: uuid.UUID,
    ) -> list[Establishment]:
        stmt = select(Establishment).where(
            Establishment.organization_id == organization_id,
            Establishment.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_subscription(
        self,
        subscription_id: uuid.UUID,
    ) -> Establishment | None:
        stmt = select(Establishment).where(
            Establishment.subscription_id == subscription_id,
            Establishment.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()