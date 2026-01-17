from pydantic import BaseModel
from datetime import datetime


class AlertOut(BaseModel):
    id: int
    rule_id: str
    severity: str
    packet_type: str
    field: str
    message: str
    first_seen: datetime
    last_seen: datetime
    status: str
