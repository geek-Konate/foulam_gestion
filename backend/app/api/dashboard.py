import uuid

from fastapi import APIRouter, Depends

from app.api.deps import (
    get_current_user_id,
    get_academic_year_repository,
    get_class_repository,
    get_student_repository,
    get_teacher_assignment_repository,
    get_fee_type_repository,
    get_payment_repository,
    get_rbac_service,
)

from app.repositories.student import (
    AcademicYearRepository,
    ClassRepository,
    StudentRepository,
)

from app.repositories.curriculum import (
    TeacherAssignmentRepository,
)

from app.repositories.finance import (
    FeeTypeRepository,
    PaymentRepository,
)

from app.schemas.dashboard import EstablishmentDashboardRead, TeacherDashboardRead

from app.services.dashboard import DashboardService, TeacherDashboardService, get_teacher_dashboard_service
from app.services.rbac_service import RbacService

router = APIRouter()


def get_dashboard_service(
    academic_year_repo: AcademicYearRepository = Depends(
        get_academic_year_repository
    ),
    class_repo: ClassRepository = Depends(
        get_class_repository
    ),
    student_repo: StudentRepository = Depends(
        get_student_repository
    ),
    teacher_assignment_repo: TeacherAssignmentRepository = Depends(
        get_teacher_assignment_repository
    ),
    fee_type_repo: FeeTypeRepository = Depends(
        get_fee_type_repository
    ),
    payment_repo: PaymentRepository = Depends(
        get_payment_repository
    ),
):
    return DashboardService(
        academic_year_repo=academic_year_repo,
        class_repo=class_repo,
        student_repo=student_repo,
        teacher_assignment_repo=teacher_assignment_repo,
        fee_type_repo=fee_type_repo,
        payment_repo=payment_repo,
    )


@router.get(
    "/establishments/{establishment_id}/dashboard",
    response_model=EstablishmentDashboardRead,
)
async def get_establishment_dashboard(
    establishment_id: uuid.UUID,
    service: DashboardService = Depends(
        get_dashboard_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="dashboard.read",
        establishment_id=establishment_id,
    )

    return await service.get_establishment_dashboard(
        establishment_id=establishment_id,
    )


@router.get(
    "/establishments/{establishment_id}/teachers/{teacher_id}/dashboard",
    response_model=TeacherDashboardRead,
)
async def get_teacher_dashboard(
    establishment_id: uuid.UUID,
    teacher_id: uuid.UUID,
    service: TeacherDashboardService = Depends(
        get_teacher_dashboard_service
    ),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    await rbac_service.require_permission(
        user_id=current_user_id,
        permission_code="dashboard.read",
        establishment_id=establishment_id,
    )

    return await service.get_teacher_dashboard(
        establishment_id=establishment_id,
        teacher_id=teacher_id,
    )