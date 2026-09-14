import uuid

from pydantic import BaseModel, EmailStr

from app.schemas.base import TimestampRead
from app.schemas.organization import EstablishmentRead, OrganizationRead


class OnboardingRequestCreate(BaseModel):
    organization_name: str
    country: str
    city: str

    contact_first_name: str
    contact_last_name: str
    contact_email: EmailStr
    contact_phone: str | None = None

    establishment_name: str
    requested_plan: str

    message: str | None = None


class OnboardingRequestRead(TimestampRead):
    organization_name: str
    country: str
    city: str

    contact_first_name: str
    contact_last_name: str
    contact_email: EmailStr
    contact_phone: str | None

    establishment_name: str
    requested_plan: str

    status: str
    rejection_reason: str | None
    resulting_organization_id: uuid.UUID | None


class OnboardingRejectPayload(BaseModel):
    rejection_reason: str


class OnboardingApprovalRead(BaseModel):
    organization: OrganizationRead
    establishment: EstablishmentRead
    owner_user_id: uuid.UUID