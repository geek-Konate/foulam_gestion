
import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.base import ORMBase, TimestampRead


# ============================================================
# ORGANIZATION
# ============================================================

class OrganizationCreate(BaseModel):
    name: str
    slug: str
    country: str
    city: str
    status: str = "active"


class OrganizationUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    country: str | None = None
    city: str | None = None
    status: str | None = None


class OrganizationRead(TimestampRead):
    name: str
    slug: str
    country: str
    city: str
    status: str

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# SUBSCRIPTION
# ============================================================

class SubscriptionCreate(BaseModel):
    plan: str
    status: str = "active"
    start_date: date
    end_date: date | None = None


class SubscriptionUpdate(BaseModel):
    plan: str | None = None
    status: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class SubscriptionRead(TimestampRead):
    organization_id: uuid.UUID
    plan: str
    status: str
    start_date: date
    end_date: date | None

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# ESTABLISHMENT
# ============================================================

class EstablishmentCreate(BaseModel):
    subscription_id: uuid.UUID
    name: str
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    status: str = "active"


class EstablishmentUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    status: str | None = None


class EstablishmentRead(TimestampRead):
    organization_id: uuid.UUID
    subscription_id: uuid.UUID
    name: str
    address: str | None
    phone: str | None
    email: EmailStr | None
    status: str

    model_config = ConfigDict(from_attributes=True)

