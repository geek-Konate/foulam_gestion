import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class RequestStatus(str, PyEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class OnboardingRequest(BaseModel):
    __tablename__ = "onboarding_requests"

    # ─────────────────────────────────────────────
    # ORGANIZATION
    # ─────────────────────────────────────────────

    organization_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # ─────────────────────────────────────────────
    # CONTACT / FUTUR PROMOTEUR
    # ─────────────────────────────────────────────

    contact_first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    contact_last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    contact_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    contact_phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    # ─────────────────────────────────────────────
    # ESTABLISHMENT
    # ─────────────────────────────────────────────

    establishment_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ─────────────────────────────────────────────
    # ABONNEMENT
    # ─────────────────────────────────────────────

    requested_plan: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # ─────────────────────────────────────────────
    # DEMANDE
    # ─────────────────────────────────────────────

    message: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    status: Mapped[RequestStatus] = mapped_column(
        Enum(
            RequestStatus,
            name="request_status",
        ),
        nullable=False,
        default=RequestStatus.PENDING,
    )

    # ─────────────────────────────────────────────
    # REVIEW
    # ─────────────────────────────────────────────

    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # ─────────────────────────────────────────────
    # RESULTAT DE L'ONBOARDING
    # ─────────────────────────────────────────────

    resulting_organization_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=True,
    )

    # ─────────────────────────────────────────────
    # RELATIONSHIPS
    # ─────────────────────────────────────────────

    reviewer: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[reviewed_by],
    )

    resulting_organization: Mapped["Organization | None"] = relationship(
        "Organization",
        foreign_keys=[resulting_organization_id],
    )