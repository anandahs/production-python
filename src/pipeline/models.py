"""The data boundary for records coming from the ingestion API.

Every record from infra/mock-api gets checked against this model before
anything downstream trusts it. This mirrors exactly what you built in
Module 2's lab - a pydantic model at the point untrusted data enters the
system - just applied to the capstone's real data source instead of the
lab's practice one.
"""
from datetime import datetime
from typing import Literal  
from pydantic import BaseModel


class RecordPayload(BaseModel):
    channel: Literal["web", "mobile", "pos", "api"]
    retry_count: int

class IngestionRecord(BaseModel):
    external_id: str
    customer_id: str
    amount: float
    status: Literal["pending", "completed", "failed", "refunded"]
    source_created_at: datetime
    source_updated_at: datetime
    payload: RecordPayload