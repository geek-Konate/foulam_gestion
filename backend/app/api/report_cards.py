import uuid

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import (
    get_current_user_id,
    get_report_card_repository,
    get_student_repository,
    get_enrollment_repository,
    get_academic_year_repository,
    get_rbac_service,
)

from app.repositories.academic import ReportCardRepository
from app.repositories.student import (
    StudentRepository,
    EnrollmentRepository,
    AcademicYearRepository,
)

from app.schemas.academic import (
    ReportCardCreate,
    ReportCardRead,
)

from app.services.report_card import ReportCardService
from app.services.rbac_service import RbacService


router = APIRouter(
    tags=["report-cards"],
)


def get_report_card_service(
    report_card_repo: ReportCardRepository = Depends(
        get_report_card_repository
    ),
    student_repo: StudentRepository = Depends(
        get_student_repository
    ),
    enrollment_repo: EnrollmentRepository = Depends(
        get_enrollment_repository
    ),
    academic_year_repo: AcademicYearRepository = Depends(
        get_academic_year_repository
    ),
):
    return ReportCardService(
        report_card_repo=report_card_repo,
        student_repo=student_repo,
        enrollment_repo=enrollment_repo,
        academic_year_repo=academic_year_repo,
    )


@router.post(
    "/establishments/{establishment_id}/report-cards",
    response_model=ReportCardRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_report_card(
    establishment_id: uuid.UUID,
    data: ReportCardCreate,
    service: ReportCardService = Depends(
        get_report_card_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="report_card.generate",
        establishment_id=establishment_id,
    )

    return await service.generate(
        establishment_id=establishment_id,
        data=data,
    )


@router.get(
    "/establishments/{establishment_id}/report-cards/{report_card_id}",
    response_model=ReportCardRead,
)
async def get_report_card(
    establishment_id: uuid.UUID,
    report_card_id: uuid.UUID,
    service: ReportCardService = Depends(
        get_report_card_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="report_card.read",
        establishment_id=establishment_id,
    )

    return await service.get(
        establishment_id=establishment_id,
        report_card_id=report_card_id,
    )


@router.get(
    "/establishments/{establishment_id}/students/{student_id}/report-cards",
    response_model=list[ReportCardRead],
)
async def list_student_report_cards(
    establishment_id: uuid.UUID,
    student_id: uuid.UUID,
    academic_year_id: uuid.UUID | None = None,
    service: ReportCardService = Depends(
        get_report_card_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="report_card.read",
        establishment_id=establishment_id,
    )

    return await service.list_by_student(
        establishment_id=establishment_id,
        student_id=student_id,
        academic_year_id=academic_year_id,
    )