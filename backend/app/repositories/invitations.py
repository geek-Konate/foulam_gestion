import uuid

from sqlalchemy import select

from app.models.invitation import Invitation
from app.repositories.base import BaseRepository


class InvitationRepository(BaseRepository[Invitation]):
    model = Invitation

    async def get_by_token_hash(
        self,
        token_hash: str,
    ) -> Invitation | None:
        stmt = select(Invitation).where(
            Invitation.token_hash == token_hash,
            Invitation.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_active_by_user(
        self,
        user_id: uuid.UUID,
    ) -> Invitation | None:
        stmt = (
            select(Invitation)
            .where(
                Invitation.user_id == user_id,
                Invitation.used_at.is_(None),
                Invitation.deleted_at.is_(None),
            )
            .order_by(Invitation.created_at.desc())
        )

        result = await self.session.execute(stmt)

        return result.scalars().first()