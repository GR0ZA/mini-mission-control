from abc import ABC, abstractmethod


class TelemetryDecoder(ABC):
    packet_id: int

    @abstractmethod
    def decode(self, payload: bytes):
        pass
