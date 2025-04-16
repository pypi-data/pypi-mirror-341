"""This module contains the API routes for computing detection metrics."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

metrics_router = APIRouter()


# TODO(Michal, 04/2025): Move to models module or metrics computation module.
class DetectionMetricsMAPRequest(BaseModel):
    """Request for computing the MAP detection metric."""

    ground_truth_task_id: UUID
    prediction_task_id: UUID


class DetectionMetricsMAPResponse(BaseModel):
    """Response for computing the MAP detection metric."""

    value: float
    per_class: dict[str, float] | None = None


@metrics_router.post(
    "/metrics/compute/detection/map", response_model=DetectionMetricsMAPResponse
)
def compute_detection_map(
    _request: DetectionMetricsMAPRequest,
) -> DetectionMetricsMAPResponse:
    """Compute the MAP detection metric."""
    return DetectionMetricsMAPResponse(
        value=0.11,
        per_class={
            "car": 0.22,
            "bus": 0.33,
            "person": 0.44,
        },
    )
