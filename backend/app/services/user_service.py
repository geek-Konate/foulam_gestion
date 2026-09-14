import secrets
import uuid

from sqlalchemy import select

from app.core.exceptions import ConflictException, NotFoundException
from app.core.security import hash_password
from app.models.rbac import Role, User, UserEstablishment, UserRole
from app.repositories.rbac import RoleRepository, UserRepository
from app.schemas.rbac import UserCreate, UserUpdate
from app.services.email_service import EmailService
from app.services.invitation_service import InvitationService
from app.services.rbac_service import RbacService


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        role_repo: RoleRepository,
        rbac_service: RbacService,
        invitation_service: InvitationService,
        email_service: EmailService,
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.rbac_service = rbac_service
        self.invitation_service = invitation_service
        self.email_service = email_service

    async def create_user(
        self,
        establishment_id: uuid.UUID,
        data: UserCreate,
    ):
        existing = await self.user_repo.get_by_email(data.email)

        if existing:
            raise ConflictException(
                "Cet email est déjà utilisé"
            )

        role = await self.role_repo.get(data.role_id)

        if not role:
            raise NotFoundException(
                "Rôle introuvable"
            )

        if role.establishment_id != establishment_id:
            raise ConflictException(
                "Ce rôle n'appartient pas à cet établissement"
            )

        if role.deleted_at is not None:
            raise NotFoundException(
                "Rôle introuvable"
            )

        user = await self.user_repo.create(
            {
                "first_name": data.first_name,
                "last_name": data.last_name,
                "email": data.email,
                "phone": data.phone,
                "password_hash": hash_password(
                    secrets.token_urlsafe(32)
                ),
                "status": "pending",
            }
        )

        self.user_repo.session.add(
            UserEstablishment(
                user_id=user.id,
                establishment_id=establishment_id,
            )
        )

        await self.user_repo.session.flush()

        await self.user_repo.session.refresh(user)

        await self.rbac_service.assign_role_to_user(
            user_id=user.id,
            role_id=role.id,
            establishment_id=establishment_id,
        )

        invitation_token = await self.invitation_service.create_invitation(
            user.id
        )

        await self.email_service.send_invitation_email(
            recipient_email=user.email,
            recipient_name=f"{user.first_name} {user.last_name}",
            invitation_token=invitation_token,
        )

        return user

    async def list_users(
        self,
        establishment_id: uuid.UUID,
    ):
        stmt = (
            select(User)
            .join(
                UserEstablishment,
                UserEstablishment.user_id == User.id,
            )
            .where(
                UserEstablishment.establishment_id == establishment_id,
                User.deleted_at.is_(None),
            )
        )

        result = await self.user_repo.session.execute(stmt)

        return list(result.scalars().all())

    async def get_user(
        self,
        establishment_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        stmt = (
            select(User)
            .join(
                UserEstablishment,
                UserEstablishment.user_id == User.id,
            )
            .where(
                User.id == user_id,
                UserEstablishment.establishment_id == establishment_id,
                User.deleted_at.is_(None),
            )
        )

        result = await self.user_repo.session.execute(stmt)

        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundException(
                "Utilisateur introuvable dans cet établissement"
            )

        return user

    async def update_user(
        self,
        establishment_id: uuid.UUID,
        user_id: uuid.UUID,
        data: UserUpdate,
    ):
        user = await self.get_user(
            establishment_id,
            user_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        return await self.user_repo.update(
            user,
            update_data,
        )

    async def delete_user(
        self,
        establishment_id: uuid.UUID,
        user_id: uuid.UUID,
    ):
        user = await self.get_user(
            establishment_id,
            user_id,
        )

        return await self.user_repo.soft_delete(user)