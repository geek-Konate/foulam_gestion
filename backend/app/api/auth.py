import uuid
from sqlalchemy import  select
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_context, get_current_user, get_rbac_service
from app.core.database import get_db
from app.core.exceptions import ConflictException, ForbiddenException
from app.models import UserRole, Role
from app.models.rbac import UserEstablishment
from app.repositories.organization import EstablishmentRepository
from app.core.security import create_access_token
from app.schemas.rbac import UserCreate, UserRead, AcceptInvitation
from app.services.rbac_service import RbacService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/select-establishment/{establishment_id}")
async def select_establishment(
    establishment_id: uuid.UUID,
    ctx=Depends(get_current_context),
    session: AsyncSession = Depends(get_db),
):
    est_repo = EstablishmentRepository(session)
    establishment = await est_repo.get(establishment_id)

    if not establishment:
        raise ConflictException("Établissement introuvable")

    org_id = establishment.organization_id

    # Vérifier que l'utilisateur a accès à cet établissement
    from app.repositories.rbac import UserRepository

    allowed = False

    # Les utilisateurs PLATFORM peuvent accéder à tous les établissements
    if ctx.organization_id is None and ctx.establishment_id is None:
        # Vérifier si l'utilisateur a un rôle PLATFORM
        stmt = (
            select(UserRole)
            .join(Role, Role.id == UserRole.role_id)
            .where(
                UserRole.user_id == ctx.user_id,
                Role.scope_type == "PLATFORM",
                UserRole.deleted_at.is_(None),
                Role.deleted_at.is_(None),
            )
            .limit(1)
        )
        result = await session.execute(stmt)
        if result.scalar_one_or_none() is not None:
            allowed = True

    if not allowed:
        stmt = select(UserEstablishment).where(
        UserEstablishment.user_id == ctx.user_id,
        UserEstablishment.establishment_id == establishment_id,
        UserEstablishment.deleted_at.is_(None),
    )
    result = await session.execute(stmt)

    if result.scalar_one_or_none() is not None:
        allowed = True

    # Vérifier les rôles ORGANIZATION (si l'utilisateur a un rôle
    # ORGANIZATION pour cette organisation)
    if not allowed:
        stmt = (
            select(UserRole)
            .join(Role, Role.id == UserRole.role_id)
            .where(
                UserRole.user_id == ctx.user_id,
                Role.scope_type == "ORGANIZATION",
                Role.organization_id == org_id,
                UserRole.deleted_at.is_(None),
                Role.deleted_at.is_(None),
            )
            .limit(1)
        )
        result = await session.execute(stmt)

        if result.scalar_one_or_none() is not None:
            allowed = True

    if not allowed:
        raise ForbiddenException(
            "Vous n'avez pas accès à cet établissement"
        )

    # Tout vérifié: générer un nouveau token enrichi
    new_token = create_access_token({
        "sub": str(ctx.user_id),
        "organization_id": str(org_id),
        "establishment_id": str(establishment_id),
    })

    return {
        "access_token": new_token,
        "token_type": "bearer",
        "organization_id": str(org_id),
        "establishment": {
            "id": str(establishment.id),
            "name": establishment.name,
        },
    }


@router.post("/register", response_model=UserRead, status_code=201)
async def register(data: UserCreate, rbac_service: RbacService = Depends(get_rbac_service)):
    return await rbac_service.register_user(data)


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    return await rbac_service.authenticate(form_data.username, form_data.password)


@router.get("/me", response_model=UserRead)
async def me(current_user=Depends(get_current_user)):
    return current_user



@router.post("/accept-invitation", response_model=UserRead)
async def accept_invitation(
    data: AcceptInvitation,
    rbac_service: RbacService = Depends(get_rbac_service),
):
    return await rbac_service.accept_invitation(
        token=data.token,
        password=data.password,
    )