from dataclasses import dataclass


@dataclass(frozen=True)
class MonitoringRule:
    id: str
    packet_type: str
    field: str
    operator: str
    threshold: float
    severity: str
    enabled: bool
