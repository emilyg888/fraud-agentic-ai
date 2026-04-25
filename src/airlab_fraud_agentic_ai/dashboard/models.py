from __future__ import annotations

from pydantic import BaseModel


class CaseQueueItem(BaseModel):
    alert_id: str
    customer_id: str
    model_score: float
    threshold: float
    status: str
    triggered_features: str


class SignalDecisionRequest(BaseModel):
    run_id: str
    signal_id: str
    decision: str
    reviewer: str
    comments: str = ""
