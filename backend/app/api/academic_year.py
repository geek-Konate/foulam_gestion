import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_rbac_service
from app.core.database import get_db
from app.repositories.student import AcademicYearRepository
from app.schemas.student import AcademicYearCreate, AcademicYearRead, AcademicYearUpdate
from app.services.academic_year_service import AcademicYearService
from app.services.rbac_service import RbacService


router = APIRouter(
    prefix="/establishments",
    tags=["academic-years"],
)


def get_academic_year_service(
    session: AsyncSession = Depends(get_db),
) -> AcademicYearService:
    return AcademicYearService(
        academic_year_repo=AcademicYearRepository(session),
    )


@router.post(
    "/{establishment_id}/academic-years",
    response_model=AcademicYearRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_academic_year(
    establishment_id: uuid.UUID,
    data: AcademicYearCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: AcademicYearService = Depends(get_academic_year_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="academic_year.create",
        establishment_id=establishment_id,
    )

    return await service.create_academic_year(
        establishment_id=establishment_id,
        data=data,
    )


@router.get(
    "/{establishment_id}/academic-years",
    response_model=list[AcademicYearRead],
)
async def list_academic_years(
    establishment_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: AcademicYearService = Depends(get_academic_year_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="academic_year.read",
        establishment_id=establishment_id,
    )

    return await service.list_academic_years(
        establishment_id=establishment_id,
    )


@router.get(
    "/{establishment_id}/academic-years/{academic_year_id}",
    response_model=AcademicYearRead,
)
async def get_academic_year(
    establishment_id: uuid.UUID,
    academic_year_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: AcademicYearService = Depends(get_academic_year_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="academic_year.read",
        establishment_id=establishment_id,
    )

    return await service.get_academic_year(
        establishment_id=establishment_id,
        academic_year_id=academic_year_id,
    )


@router.patch(
    "/{establishment_id}/academic-years/{academic_year_id}",
    response_model=AcademicYearRead,
)
async def update_academic_year(
    establishment_id: uuid.UUID,
    academic_year_id: uuid.UUID,
    data: AcademicYearUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: AcademicYearService = Depends(get_academic_year_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="academic_year.update",
        establishment_id=establishment_id,
    )

    return await service.update_academic_year(
        establishment_id=establishment_id,
        academic_year_id=academic_year_id,
        data=data,
    )


@router.delete(
    "/{establishment_id}/academic-years/{academic_year_id}",
    response_model=AcademicYearRead,
)
async def delete_academic_year(
    establishment_id: uuid.UUID,
    academic_year_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
    service: AcademicYearService = Depends(get_academic_year_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="academic_year.delete",
        establishment_id=establishment_id,
    )

    return await service.delete_academic_year(
        establishment_id=establishment_id,
        academic_year_id=academic_year_id,
    )