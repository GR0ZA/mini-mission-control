from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class SpacecraftMode(Enum):
    SAFE = 0
    NORMAL = 1


@dataclass(frozen=True)
class HousekeepingTM:
    packet_id: int
    sequence: int
    timestamp: datetime
    battery_voltage_v: int
    temperature_c: int
    mode: SpacecraftMode


@dataclass(frozen=True)
class AttitudeTM:
    packet_id: int
    sequence: int
    timestamp: datetime
    roll_deg: float
    pitch_deg: float
    yaw_deg: float
