
import uuid

from fastapi import APIRouter, Depends

from app.api.deps import (
    get_current_user,
    get_organization_service,
    require_organization_permission,
    require_platform_permission,
)
from app.schemas.organization import (
    EstablishmentCreate,
    EstablishmentRead,
    EstablishmentUpdate,
    OrganizationCreate,
    OrganizationRead,
    OrganizationUpdate,
    SubscriptionCreate,
    SubscriptionRead,
    SubscriptionUpdate,
)
from app.services.organization_service import OrganizationService


router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)


# ============================================================
# ORGANIZATIONS
# ============================================================

@router.post(
    "",
    response_model=OrganizationRead,
    status_code=201,
    dependencies=[
        Depends(
            require_platform_permission(
                "organization.create"
            )
        )
    ],
)
async def create_organization(
    data: OrganizationCreate,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.create_organization(data)


@router.get(
    "",
    response_model=list[OrganizationRead],
    dependencies=[
        Depends(
            require_platform_permission(
                "organization.read"
            )
        )
    ],
)
async def list_organizations(
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.list_organizations()


@router.get(
    "/{organization_id}",
    response_model=OrganizationRead,
    dependencies=[
        Depends(
            require_organization_permission(
                "organization.read"
            )
        )
    ],
)
async def get_organization(
    organization_id: uuid.UUID,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.get_organization(
        organization_id
    )


@router.patch(
    "/{organization_id}",
    response_model=OrganizationRead,
    dependencies=[
        Depends(
            require_organization_permission(
                "organization.update"
            )
        )
    ],
)
async def update_organization(
    organization_id: uuid.UUID,
    data: OrganizationUpdate,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.update_organization(
        organization_id,
        data,
    )


@router.delete(
    "/{organization_id}",
    status_code=204,
    dependencies=[
        Depends(
            require_organization_permission(
                "organization.delete"
            )
        )
    ],
)
async def delete_organization(
    organization_id: uuid.UUID,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    await service.delete_organization(
        organization_id
    )


# ============================================================
# SUBSCRIPTIONS
# ============================================================

@router.post(
    "/{organization_id}/subscriptions",
    response_model=SubscriptionRead,
    status_code=201,
    dependencies=[
        Depends(
            require_organization_permission(
                "subscription.create"
            )
        )
    ],
)
async def create_subscription(
    organization_id: uuid.UUID,
    data: SubscriptionCreate,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.create_subscription(
        organization_id,
        data,
    )


@router.get(
    "/{organization_id}/subscriptions",
    response_model=list[SubscriptionRead],
    dependencies=[
        Depends(
            require_organization_permission(
                "subscription.read"
            )
        )
    ],
)
async def list_subscriptions(
    organization_id: uuid.UUID,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.list_subscriptions(
        organization_id
    )


@router.get(
    "/{organization_id}/subscriptions/{subscription_id}",
    response_model=SubscriptionRead,
    dependencies=[
        Depends(
            require_organization_permission(
                "subscription.read"
            )
        )
    ],
)
async def get_subscription(
    organization_id: uuid.UUID,
    subscription_id: uuid.UUID,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.get_subscription(
        organization_id,
        subscription_id,
    )


@router.patch(
    "/{organization_id}/subscriptions/{subscription_id}",
    response_model=SubscriptionRead,
    dependencies=[
        Depends(
            require_organization_permission(
                "subscription.update"
            )
        )
    ],
)
async def update_subscription(
    organization_id: uuid.UUID,
    subscription_id: uuid.UUID,
    data: SubscriptionUpdate,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.update_subscription(
        organization_id,
        subscription_id,
        data,
    )


@router.delete(
    "/{organization_id}/subscriptions/{subscription_id}",
    status_code=204,
    dependencies=[
        Depends(
            require_organization_permission(
                "subscription.delete"
            )
        )
    ],
)
async def delete_subscription(
    organization_id: uuid.UUID,
    subscription_id: uuid.UUID,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    await service.delete_subscription(
        organization_id,
        subscription_id,
    )


# ============================================================
# ESTABLISHMENTS
# ============================================================

@router.post(
    "/{organization_id}/establishments",
    response_model=EstablishmentRead,
    status_code=201,
    dependencies=[
        Depends(
            require_organization_permission(
                "establishment.create"
            )
        )
    ],
)
async def create_establishment(
    organization_id: uuid.UUID,
    data: EstablishmentCreate,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.create_establishment(
        organization_id,
        data,
    )


@router.get(
    "/{organization_id}/establishments",
    response_model=list[EstablishmentRead],
    dependencies=[
        Depends(
            require_organization_permission(
                "establishment.read"
            )
        )
    ],
)
async def list_establishments(
    organization_id: uuid.UUID,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.list_establishments_for_organization(
        organization_id
    )


@router.get(
    "/{organization_id}/establishments/{establishment_id}",
    response_model=EstablishmentRead,
    dependencies=[
        Depends(
            require_organization_permission(
                "establishment.read"
            )
        )
    ],
)
async def get_establishment(
    organization_id: uuid.UUID,
    establishment_id: uuid.UUID,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.get_establishment(
        organization_id,
        establishment_id,
    )


@router.patch(
    "/{organization_id}/establishments/{establishment_id}",
    response_model=EstablishmentRead,
    dependencies=[
        Depends(
            require_organization_permission(
                "establishment.update"
            )
        )
    ],
)
async def update_establishment(
    organization_id: uuid.UUID,
    establishment_id: uuid.UUID,
    data: EstablishmentUpdate,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    return await service.update_establishment(
        organization_id,
        establishment_id,
        data,
    )


@router.delete(
    "/{organization_id}/establishments/{establishment_id}",
    status_code=204,
    dependencies=[
        Depends(
            require_organization_permission(
                "establishment.delete"
            )
        )
    ],
)
async def delete_establishment(
    organization_id: uuid.UUID,
    establishment_id: uuid.UUID,
    service: OrganizationService = Depends(
        get_organization_service
    ),
    current_user=Depends(get_current_user),
):
    await service.delete_establishment(
        organization_id,
        establishment_id,
    )
