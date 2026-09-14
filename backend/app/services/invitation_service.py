import hashlib
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from app.core.exceptions import ConflictException, NotFoundException
from app.core.security import hash_password
from app.repositories.invitations import InvitationRepository


INVITATION_EXPIRE_HOURS = 48


class InvitationService:
    def __init__(
        self,
        invitation_repo: InvitationRepository,
    ):
        self.invitation_repo = invitation_repo

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()

    async def create_invitation(
        self,
        user_id: uuid.UUID,
    ) -> str:
        existing = await self.invitation_repo.get_active_by_user(
            user_id
        )

        if existing:
            raise ConflictException(
                "Une invitation active existe déjà pour cet utilisateur"
            )

        token = self.generate_token()
        token_hash = self.hash_token(token)

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(hours=INVITATION_EXPIRE_HOURS)
        )

        await self.invitation_repo.create(
            {
                "user_id": user_id,
                "token_hash": token_hash,
                "expires_at": expires_at,
            }
        )

        return token

    async def get_valid_invitation(
        self,
        token: str,
    ):
        token_hash = self.hash_token(token)

        invitation = await self.invitation_repo.get_by_token_hash(
            token_hash
        )

        if not invitation:
            raise NotFoundException(
                "Invitation invalide ou introuvable"
            )

        if invitation.used_at is not None:
            raise ConflictException(
                "Cette invitation a déjà été utilisée"
            )

        now = datetime.now(timezone.utc)

        if invitation.expires_at <= now:
            raise ConflictException(
                "Cette invitation a expiré"
            )

        return invitation

    async def consume_invitation(
        self,
        invitation,
    ):
        if invitation.used_at is not None:
            raise ConflictException(
                "Cette invitation a déjà été utilisée"
            )

        invitation.used_at = datetime.now(timezone.utc)

        await self.invitation_repo.session.flush()
        await self.invitation_repo.session.refresh(invitation)

        return invitation

