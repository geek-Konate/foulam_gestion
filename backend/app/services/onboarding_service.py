import re
import unicodedata
import uuid
from datetime import date, datetime, timezone

from app.core.exceptions import ConflictException, NotFoundException
from app.core.security import hash_password
from app.models.onboarding import RequestStatus
from app.repositories.invitations import InvitationRepository
from app.repositories.onboarding import OnboardingRequestRepository
from app.repositories.organization import (
    EstablishmentRepository,
    OrganizationRepository,
    SubscriptionRepository,
)
from app.repositories.rbac import (
    RoleRepository,
    UserRepository,
    UserRoleRepository,
)
from app.schemas.onboarding import OnboardingRequestCreate
from app.services.email_service import EmailService
from app.services.invitation_service import InvitationService
from app.services.rbac_service import RbacService


class OnboardingService:
    def __init__(
        self,
        request_repo: OnboardingRequestRepository,
        org_repo: OrganizationRepository,
        sub_repo: SubscriptionRepository,
        est_repo: EstablishmentRepository,
        user_repo: UserRepository,
        role_repo: RoleRepository,
        user_role_repo: UserRoleRepository,
        invitation_repo: InvitationRepository,
        invitation_service: InvitationService,
        email_service: EmailService,
        rbac_service: RbacService,
    ):
        self.request_repo = request_repo
        self.org_repo = org_repo
        self.sub_repo = sub_repo
        self.est_repo = est_repo
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.user_role_repo = user_role_repo
        self.invitation_repo = invitation_repo
        self.invitation_service = invitation_service
        self.email_service = email_service
        self.rbac_service = rbac_service

    @staticmethod
    def generate_slug(name: str) -> str:
        value = unicodedata.normalize("NFKD", name)
        value = value.encode("ascii", "ignore").decode("ascii")
        value = value.lower()
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-")

    async def submit_request(
        self,
        data: OnboardingRequestCreate,
    ):
        return await self.request_repo.create(
            data.model_dump()
        )

    async def list_pending_requests(
        self,
        current_user_id: uuid.UUID,
    ):
        await self.rbac_service.require_permission(
            current_user_id,
            "onboarding.review",
        )

        return await self.request_repo.list_pending()

    async def approve_request(
        self,
        request_id: uuid.UUID,
        current_user_id: uuid.UUID,
    ):
        await self.rbac_service.require_permission(
            current_user_id,
            "onboarding.review",
        )

        req = await self.request_repo.get(request_id)

        if not req:
            raise NotFoundException(
                "Demande introuvable"
            )

        if req.status != RequestStatus.PENDING:
            raise ConflictException(
                "Cette demande a déjà été traitée"
            )

        existing_user = await self.user_repo.get_by_email(
            req.contact_email
        )

        if existing_user:
            raise ConflictException(
                "Un compte existe déjà avec cet email"
            )

        # ─────────────────────────────────────────────
        # 1. CRÉER LE COMPTE DU PROMOTEUR
        # ─────────────────────────────────────────────

        owner = await self.user_repo.create(
            {
                "first_name": req.contact_first_name,
                "last_name": req.contact_last_name,
                "email": req.contact_email,
                "password_hash": hash_password(
                    uuid.uuid4().hex
                ),
                "status": "active",
            }
        )

        # ─────────────────────────────────────────────
        # 2. CRÉER L'ORGANISATION
        # ─────────────────────────────────────────────

        slug = self.generate_slug(
            req.organization_name
        )

        existing_slug = await self.org_repo.get_by_slug(
            slug
        )

        if existing_slug:
            slug = f"{slug}-{uuid.uuid4().hex[:8]}"

        org = await self.org_repo.create(
            {
                "name": req.organization_name,
                "slug": slug,
                "country": req.country,
                "city": req.city,
                "status": "active",
            }
        )

        # ─────────────────────────────────────────────
        # 3. CRÉER L'ABONNEMENT
        # ─────────────────────────────────────────────

        subscription = await self.sub_repo.create(
            {
                "organization_id": org.id,
                "plan": req.requested_plan,
                "status": "active",
                "start_date": date.today(),
            }
        )

        # ─────────────────────────────────────────────
        # 4. CRÉER L'ÉTABLISSEMENT
        # ─────────────────────────────────────────────

        establishment = await self.est_repo.create(
            {
                "organization_id": org.id,
                "subscription_id": subscription.id,
                "name": req.establishment_name,
                "email": req.contact_email,
            }
        )

        # ─────────────────────────────────────────────
        # 5. CRÉER LE RÔLE ADMINISTRATEUR
        # ─────────────────────────────────────────────

        roles = await self.role_repo.get_by_scope(
            "ESTABLISHMENT",
            establishment_id=establishment.id,
        )

        if roles:
            admin_role = roles[0]
        else:
            admin_role = await self.role_repo.create({
                "name": "establishment_admin",
                "description": "Administrateur de l'établissement",
                "scope_type": "ESTABLISHMENT",
                "establishment_id": establishment.id,
                "is_system": True,
            })

        await self.rbac_service.assign_default_establishment_admin_permissions(
            admin_role.id
        )

        await self.user_role_repo.create({
            "user_id": owner.id,
            "role_id": admin_role.id,
            "establishment_id": establishment.id,
        })

        # ─────────────────────────────────────────────
        # 7. CRÉER L'INVITATION
        # ─────────────────────────────────────────────

        invitation_token = (
            await self.invitation_service.create_invitation(
                owner.id
            )
        )

        # ─────────────────────────────────────────────
        # 8. ENVOYER L'EMAIL
        # ─────────────────────────────────────────────

        await self.email_service.send_invitation_email(
            recipient_email=owner.email,
            recipient_name=(
                f"{owner.first_name} {owner.last_name}"
            ),
            invitation_token=invitation_token,
        )

        # ─────────────────────────────────────────────
        # 9. CLÔTURER LA DEMANDE
        # ─────────────────────────────────────────────

        req.status = RequestStatus.APPROVED
        req.reviewed_by = current_user_id
        req.reviewed_at = datetime.now(timezone.utc)
        req.resulting_organization_id = org.id

        await self.request_repo.session.flush()
        await self.request_repo.session.refresh(req)

        return {
            "organization": org,
            "establishment": establishment,
            "owner_user_id": owner.id,
        }

    async def reject_request(
        self,
        request_id: uuid.UUID,
        reason: str,
        current_user_id: uuid.UUID,
    ):
        await self.rbac_service.require_permission(
            current_user_id,
            "onboarding.review",
        )

        req = await self.request_repo.get(request_id)

        if not req:
            raise NotFoundException(
                "Demande introuvable"
            )

        if req.status != RequestStatus.PENDING:
            raise ConflictException(
                "Cette demande a déjà été traitée"
            )

        req.status = RequestStatus.REJECTED
        req.reviewed_by = current_user_id
        req.reviewed_at = datetime.now(timezone.utc)
        req.rejection_reason = reason

        await self.request_repo.session.flush()
        await self.request_repo.session.refresh(req)

        return req