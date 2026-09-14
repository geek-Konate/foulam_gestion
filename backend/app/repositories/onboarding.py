from sqlalchemy import select

from app.models.onboarding import OnboardingRequest, RequestStatus
from app.repositories.base import BaseRepository


class OnboardingRequestRepository(BaseRepository[OnboardingRequest]):
    model = OnboardingRequest

    async def list_pending(self) -> list[OnboardingRequest]:
        stmt = select(OnboardingRequest).where(
            OnboardingRequest.status == RequestStatus.PENDING,
            OnboardingRequest.deleted_at.is_(None),
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())