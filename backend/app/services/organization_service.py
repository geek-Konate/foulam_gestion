
import uuid

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.organization import (
    EstablishmentRepository,
    OrganizationRepository,
    SubscriptionRepository,
)
from app.schemas.organization import (
    EstablishmentCreate,
    EstablishmentUpdate,
    OrganizationCreate,
    OrganizationUpdate,
    SubscriptionCreate,
    SubscriptionUpdate,
)


class OrganizationService:
    def __init__(
        self,
        org_repo: OrganizationRepository,
        sub_repo: SubscriptionRepository,
        est_repo: EstablishmentRepository,
    ):
        self.org_repo = org_repo
        self.sub_repo = sub_repo
        self.est_repo = est_repo

    # ============================================================
    # ORGANIZATION
    # ============================================================

    async def create_organization(
        self,
        data: OrganizationCreate,
    ):
        existing = await self.org_repo.get_by_name(data.name)

        if existing:
            raise ConflictException(
                f"Une organisation nommée '{data.name}' existe déjà"
            )

        existing_slug = await self.org_repo.get_by_slug(data.slug)

        if existing_slug:
            raise ConflictException(
                f"Le slug '{data.slug}' est déjà utilisé"
            )

        return await self.org_repo.create(
            data.model_dump()
        )

    async def list_organizations(self):
        return await self.org_repo.list()

    async def get_organization(
        self,
        organization_id: uuid.UUID,
    ):
        organization = await self.org_repo.get(
            organization_id
        )

        if not organization:
            raise NotFoundException(
                "Organisation introuvable"
            )

        return organization

    async def update_organization(
        self,
        organization_id: uuid.UUID,
        data: OrganizationUpdate,
    ):
        organization = await self.get_organization(
            organization_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "slug" in update_data:
            existing_slug = await self.org_repo.get_by_slug(
                update_data["slug"]
            )

            if (
                existing_slug
                and existing_slug.id != organization_id
            ):
                raise ConflictException(
                    f"Le slug '{update_data['slug']}' est déjà utilisé"
                )

        return await self.org_repo.update(
            organization,
            update_data,
        )

    async def delete_organization(
        self,
        organization_id: uuid.UUID,
    ):
        organization = await self.get_organization(
            organization_id
        )

        return await self.org_repo.soft_delete(
            organization
        )

    # ============================================================
    # SUBSCRIPTION
    # ============================================================

    async def create_subscription(
        self,
        organization_id: uuid.UUID,
        data: SubscriptionCreate,
    ):
        await self.get_organization(
            organization_id
        )

        subscription_data = data.model_dump()
        subscription_data["organization_id"] = organization_id

        return await self.sub_repo.create(
            subscription_data
        )

    async def list_subscriptions(
        self,
        organization_id: uuid.UUID,
    ):
        await self.get_organization(
            organization_id
        )

        return await self.sub_repo.get_active_by_organization(
            organization_id
        )

    async def get_subscription(
        self,
        organization_id: uuid.UUID,
        subscription_id: uuid.UUID,
    ):
        subscription = await self.sub_repo.get(
            subscription_id
        )

        if not subscription:
            raise NotFoundException(
                "Abonnement introuvable"
            )

        if subscription.organization_id != organization_id:
            raise NotFoundException(
                "Abonnement introuvable"
            )

        return subscription

    async def update_subscription(
        self,
        organization_id: uuid.UUID,
        subscription_id: uuid.UUID,
        data: SubscriptionUpdate,
    ):
        subscription = await self.get_subscription(
            organization_id,
            subscription_id,
        )

        return await self.sub_repo.update(
            subscription,
            data.model_dump(
                exclude_unset=True
            ),
        )

    async def delete_subscription(
        self,
        organization_id: uuid.UUID,
        subscription_id: uuid.UUID,
    ):
        subscription = await self.get_subscription(
            organization_id,
            subscription_id,
        )

        return await self.sub_repo.soft_delete(
            subscription
        )

    # ============================================================
    # ESTABLISHMENT
    # ============================================================

    async def create_establishment(
        self,
        organization_id: uuid.UUID,
        data: EstablishmentCreate,
    ):
        await self.get_organization(
            organization_id
        )

        subscription = await self.sub_repo.get(
            data.subscription_id
        )

        if not subscription:
            raise NotFoundException(
                "Abonnement introuvable"
            )

        if subscription.organization_id != organization_id:
            raise ConflictException(
                "Cet abonnement n'appartient pas à cette organisation"
            )

        existing = await self.est_repo.get_by_subscription(
            data.subscription_id
        )

        if existing:
            raise ConflictException(
                "Cet abonnement est déjà lié à un établissement"
            )

        establishment_data = data.model_dump()
        establishment_data["organization_id"] = organization_id

        return await self.est_repo.create(
            establishment_data
        )

    async def list_establishments_for_organization(
        self,
        organization_id: uuid.UUID,
    ):
        await self.get_organization(
            organization_id
        )

        return await self.est_repo.get_by_organization(
            organization_id
        )

    async def get_establishment(
        self,
        organization_id: uuid.UUID,
        establishment_id: uuid.UUID,
    ):
        establishment = await self.est_repo.get(
            establishment_id
        )

        if not establishment:
            raise NotFoundException(
                "Établissement introuvable"
            )

        if establishment.organization_id != organization_id:
            raise NotFoundException(
                "Établissement introuvable"
            )

        return establishment

    async def update_establishment(
        self,
        organization_id: uuid.UUID,
        establishment_id: uuid.UUID,
        data: EstablishmentUpdate,
    ):
        establishment = await self.get_establishment(
            organization_id,
            establishment_id,
        )

        return await self.est_repo.update(
            establishment,
            data.model_dump(
                exclude_unset=True
            ),
        )

    async def delete_establishment(
        self,
        organization_id: uuid.UUID,
        establishment_id: uuid.UUID,
    ):
        establishment = await self.get_establishment(
            organization_id,
            establishment_id,
        )

        return await self.est_repo.soft_delete(
            establishment
        )
