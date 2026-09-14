import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_current_user_id,
    get_rbac_service,
)
from app.core.database import get_db
from app.repositories.invitations import InvitationRepository
from app.repositories.rbac import RoleRepository, UserRepository
from app.schemas.rbac import UserCreate, UserRead, UserUpdate
from app.services.email_service import EmailService
from app.services.invitation_service import InvitationService
from app.services.rbac_service import RbacService
from app.services.user_service import UserService


router = APIRouter(
    prefix="/establishments",
    tags=["users"],
)


def get_user_service(
    session: AsyncSession = Depends(get_db),
    rbac_service: RbacService = Depends(get_rbac_service),
) -> UserService:
    invitation_repo = InvitationRepository(session)

    return UserService(
        user_repo=UserRepository(session),
        role_repo=RoleRepository(session),
        rbac_service=rbac_service,
        invitation_service=InvitationService(invitation_repo),
        email_service=EmailService(),
    )


@router.post(
    "/{establishment_id}/users",
    response_model=UserRead,
    status_code=201,
)
async def create_user(
    establishment_id: uuid.UUID,
    data: UserCreate,
    user_service: UserService = Depends(get_user_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    await user_service.rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="user.create",
        establishment_id=establishment_id,
    )

    return await user_service.create_user(
        establishment_id,
        data,
    )


@router.get(
    "/{establishment_id}/users",
    response_model=list[UserRead],
)
async def list_users(
    establishment_id: uuid.UUID,
    user_service: UserService = Depends(get_user_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    await user_service.rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="user.read",
        establishment_id=establishment_id,
    )

    return await user_service.list_users(
        establishment_id
    )


@router.get(
    "/{establishment_id}/users/{user_id}",
    response_model=UserRead,
)
async def get_user(
    establishment_id: uuid.UUID,
    user_id: uuid.UUID,
    user_service: UserService = Depends(get_user_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    await user_service.rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="user.read",
        establishment_id=establishment_id,
    )

    return await user_service.get_user(
        establishment_id,
        user_id,
    )


@router.patch(
    "/{establishment_id}/users/{user_id}",
    response_model=UserRead,
)
async def update_user(
    establishment_id: uuid.UUID,
    user_id: uuid.UUID,
    data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    await user_service.rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="user.update",
        establishment_id=establishment_id,
    )

    return await user_service.update_user(
        establishment_id,
        user_id,
        data,
    )


@router.delete(
    "/{establishment_id}/users/{user_id}",
    status_code=204,
)
async def delete_user(
    establishment_id: uuid.UUID,
    user_id: uuid.UUID,
    user_service: UserService = Depends(get_user_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    await user_service.rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="user.delete",
        establishment_id=establishment_id,
    )

    await user_service.delete_user(
        establishment_id,
        user_id,
    )