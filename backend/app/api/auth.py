from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_current_user, get_rbac_service
from app.schemas.rbac import UserCreate, UserRead, AcceptInvitation
from app.services.rbac_service import RbacService

router = APIRouter(prefix="/auth", tags=["auth"])


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