import uuid

from dataclasses import dataclass

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token

from app.repositories.academic import EvaluationRepository, GradeRepository, AttendanceRepository, ReportCardRepository
from app.repositories.curriculum import CurriculumRepository, CurriculumSubjectRepository, SubjectRepository, \
    ClassCurriculumRepository, TeacherAssignmentRepository
from app.repositories.finance import (
    FeeTypeRepository,
    PaymentRepository,
    ReceiptRepository,
)
from app.repositories.onboarding import OnboardingRequestRepository
from app.repositories.organization import (
    EstablishmentRepository,
    OrganizationRepository,
    SubscriptionRepository,
)
from app.repositories.rbac import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    UserRepository,
    UserRoleRepository,
)
from app.repositories.student import (
    ClassRepository,
    EnrollmentRepository,
    StudentRepository, AcademicYearRepository, LevelRepository,
)

from app.services.enrollment_service import EnrollmentService
from app.services.onboarding_service import OnboardingService
from app.services.organization_service import OrganizationService
from app.services.rbac_service import RbacService

from app.repositories.invitations import InvitationRepository
from app.services.email_service import EmailService
from app.services.invitation_service import InvitationService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)


def get_rbac_service(
    session: AsyncSession = Depends(get_db),
) -> RbacService:
    invitation_repo = InvitationRepository(session)

    return RbacService(
        user_repo=UserRepository(session),
        role_repo=RoleRepository(session),
        permission_repo=PermissionRepository(session),
        role_permission_repo=RolePermissionRepository(session),
        user_role_repo=UserRoleRepository(session),
        invitation_service=InvitationService(invitation_repo),
    )


def get_organization_service(
    session: AsyncSession = Depends(get_db),
) -> OrganizationService:
    return OrganizationService(
        org_repo=OrganizationRepository(session),
        sub_repo=SubscriptionRepository(session),
        est_repo=EstablishmentRepository(session),
    )


def get_enrollment_service(
    session: AsyncSession = Depends(get_db),
    rbac_service: RbacService = Depends(get_rbac_service),
) -> EnrollmentService:
    return EnrollmentService(
        enrollment_repo=EnrollmentRepository(session),
        class_repo=ClassRepository(session),
        student_repo=StudentRepository(session),
        rbac_service=rbac_service,
    )


def get_onboarding_service(
    session: AsyncSession = Depends(get_db),
    rbac_service: RbacService = Depends(get_rbac_service),
) -> OnboardingService:
    invitation_repo = InvitationRepository(session)

    return OnboardingService(
        request_repo=OnboardingRequestRepository(session),
        org_repo=OrganizationRepository(session),
        sub_repo=SubscriptionRepository(session),
        est_repo=EstablishmentRepository(session),
        user_repo=UserRepository(session),
        role_repo=RoleRepository(session),
        user_role_repo=UserRoleRepository(session),
        invitation_repo=invitation_repo,
        invitation_service=InvitationService(invitation_repo),
        email_service=EmailService(),
        rbac_service=rbac_service,
    )

async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> uuid.UUID:
    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Token invalide ou expiré",
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Type de token invalide",
        )

    sub = payload.get("sub")

    if not sub:
        raise HTTPException(
            status_code=401,
            detail="Token malformé",
        )

    return uuid.UUID(sub)


@dataclass
class CurrentContext:
    user_id: uuid.UUID
    organization_id: uuid.UUID | None = None
    establishment_id: uuid.UUID | None = None


async def get_current_context(
    token: str = Depends(oauth2_scheme),
) -> CurrentContext:
    try:
        payload = decode_token(token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Token invalide ou expiré",
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Type de token invalide",
        )

    sub = payload.get("sub")

    if not sub:
        raise HTTPException(
            status_code=401,
            detail="Token malformé",
        )

    org_id_raw = payload.get("organization_id")
    est_id_raw = payload.get("establishment_id")

    return CurrentContext(
        user_id=uuid.UUID(sub),
        organization_id=uuid.UUID(org_id_raw) if org_id_raw else None,
        establishment_id=uuid.UUID(est_id_raw) if est_id_raw else None,
    )


async def get_current_user(
    user_id: uuid.UUID = Depends(get_current_user_id),
    rbac_service: RbacService = Depends(get_rbac_service),
):
    return await rbac_service.get_current_user(user_id)


def require_organization_permission(permission_code: str):
    async def permission_dependency(
        organization_id: uuid.UUID,
        user_id: uuid.UUID = Depends(get_current_user_id),
        rbac_service: RbacService = Depends(get_rbac_service),
    ):
        await rbac_service.require_permission(
            user_id=user_id,
            permission_code=permission_code,
            organization_id=organization_id,
        )

    return permission_dependency


def require_platform_permission(permission_code: str):
    async def permission_dependency(
        user_id: uuid.UUID = Depends(get_current_user_id),
        rbac_service: RbacService = Depends(get_rbac_service),
    ):
        await rbac_service.require_permission(
            user_id=user_id,
            permission_code=permission_code,
        )

    return permission_dependency

def get_curriculum_repository(
    session: AsyncSession = Depends(get_db),
) -> CurriculumRepository:
    return CurriculumRepository(session)


def get_academic_year_repository(
    session: AsyncSession = Depends(get_db),
) -> AcademicYearRepository:
    return AcademicYearRepository(session)


def get_level_repository(
    session: AsyncSession = Depends(get_db),
) -> LevelRepository:
    return LevelRepository(session)

def get_curriculum_subject_repository(
    session: AsyncSession = Depends(get_db),
) -> CurriculumSubjectRepository:
    return CurriculumSubjectRepository(session)


def get_subject_repository(
    session: AsyncSession = Depends(get_db),
) -> SubjectRepository:
    return SubjectRepository(session)

def get_class_repository(
    session: AsyncSession = Depends(get_db),
) -> ClassRepository:
    return ClassRepository(session)


def get_class_curriculum_repository(
    session: AsyncSession = Depends(get_db),
) -> ClassCurriculumRepository:
    return ClassCurriculumRepository(session)

def get_teacher_assignment_repository(
    session: AsyncSession = Depends(get_db),
) -> TeacherAssignmentRepository:
    return TeacherAssignmentRepository(session)


def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(session)

def get_evaluation_repository(
    session: AsyncSession = Depends(get_db),
) -> EvaluationRepository:
    return EvaluationRepository(session)

def get_grade_repository(
    session: AsyncSession = Depends(get_db),
) -> GradeRepository:
    return GradeRepository(session)


def get_evaluation_repository(
    session: AsyncSession = Depends(get_db),
) -> EvaluationRepository:
    return EvaluationRepository(session)


def get_student_repository(
    session: AsyncSession = Depends(get_db),
) -> StudentRepository:
    return StudentRepository(session)


def get_enrollment_repository(
    session: AsyncSession = Depends(get_db),
) -> EnrollmentRepository:
    return EnrollmentRepository(session)

def get_attendance_repository(
    session: AsyncSession = Depends(get_db),
) -> AttendanceRepository:
    return AttendanceRepository(session)

def get_report_card_repository(
    session=Depends(get_db),
):
    return ReportCardRepository(session)


from app.repositories.finance import (
    FeeTypeRepository,
    PaymentRepository,
    ReceiptRepository,
)


def get_fee_type_repository(
    session=Depends(get_db),
):
    return FeeTypeRepository(session)


def get_payment_repository(
    session=Depends(get_db),
):
    return PaymentRepository(session)


def get_receipt_repository(
    session=Depends(get_db),
):
    return ReceiptRepository(session)