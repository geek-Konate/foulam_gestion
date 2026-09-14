import uuid
from enum import Enum

from pydantic import BaseModel, EmailStr

from app.schemas.base import TimestampRead


# ─────────────────────────────────────────────
# SCOPE
# ─────────────────────────────────────────────

class ScopeType(str, Enum):
    PLATFORM = "PLATFORM"
    ORGANIZATION = "ORGANIZATION"
    ESTABLISHMENT = "ESTABLISHMENT"


# ─────────────────────────────────────────────
# USER
# ─────────────────────────────────────────────
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    role_id: uuid.UUID


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    status: str | None = None


class UserRead(TimestampRead):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    status: str


# ─────────────────────────────────────────────
# ROLE
# ─────────────────────────────────────────────

class RoleCreate(BaseModel):
    name: str
    description: str | None = None
    scope_type: ScopeType
    organization_id: uuid.UUID | None = None
    establishment_id: uuid.UUID | None = None


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class RoleRead(TimestampRead):
    name: str
    description: str | None
    scope_type: ScopeType
    organization_id: uuid.UUID | None
    establishment_id: uuid.UUID | None
    is_system: bool

# ─────────────────────────────────────────────
# PERMISSION
# ─────────────────────────────────────────────

class PermissionCreate(BaseModel):
    code: str
    name: str
    module: str
    description: str | None = None


class PermissionRead(TimestampRead):
    code: str
    name: str
    module: str
    description: str | None


# ─────────────────────────────────────────────
# ROLE PERMISSION
# ─────────────────────────────────────────────

class RolePermissionCreate(BaseModel):
    role_id: uuid.UUID
    permission_id: uuid.UUID


class RolePermissionRead(TimestampRead):
    role_id: uuid.UUID
    permission_id: uuid.UUID


# ─────────────────────────────────────────────
# USER ROLE
# ─────────────────────────────────────────────

class UserRoleCreate(BaseModel):
    user_id: uuid.UUID
    role_id: uuid.UUID
    organization_id: uuid.UUID | None = None
    establishment_id: uuid.UUID | None = None


class UserRoleRead(TimestampRead):
    user_id: uuid.UUID
    role_id: uuid.UUID
    organization_id: uuid.UUID | None
    establishment_id: uuid.UUID | None

class AcceptInvitation(BaseModel):
    token: str
    password: str