import uuid

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id, get_onboarding_service
from app.schemas.onboarding import (
    OnboardingApprovalRead,
    OnboardingRejectPayload,
    OnboardingRequestCreate,
    OnboardingRequestRead,
)
from app.services.onboarding_service import OnboardingService


router = APIRouter(
    prefix="/onboarding",
    tags=["onboarding"],
)


@router.post(
    "/requests",
    response_model=OnboardingRequestRead,
    status_code=201,
)
async def submit_request(
    data: OnboardingRequestCreate,
    service: OnboardingService = Depends(get_onboarding_service),
):
    return await service.submit_request(data)


@router.get(
    "/requests/pending",
    response_model=list[OnboardingRequestRead],
)
async def list_pending(
    service: OnboardingService = Depends(get_onboarding_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return await service.list_pending_requests(current_user_id)


@router.post(
    "/requests/{request_id}/approve",
    response_model=OnboardingApprovalRead,
)
async def approve(
    request_id: uuid.UUID,
    service: OnboardingService = Depends(get_onboarding_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return await service.approve_request(
        request_id,
        current_user_id,
    )


@router.post(
    "/requests/{request_id}/reject",
    response_model=OnboardingRequestRead,
)
async def reject(
    request_id: uuid.UUID,
    payload: OnboardingRejectPayload,
    service: OnboardingService = Depends(get_onboarding_service),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    return await service.reject_request(
        request_id,
        payload.rejection_reason,
        current_user_id,
    )