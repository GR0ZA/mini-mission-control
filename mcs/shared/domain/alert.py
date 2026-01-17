from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AlertStatus(Enum):
    NEW = "NEW"
    ACK = "ACK"
    CLEARED = "CLEARED"


@dataclass
class Alert:
    id: int | None
    rule_id: str
    severity: str
    packet_type: str
    field: str
    message: str
    first_seen: datetime
    last_seen: datetime
    status: AlertStatus
