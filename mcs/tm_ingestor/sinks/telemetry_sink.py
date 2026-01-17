from abc import ABC, abstractmethod


class TelemetrySink(ABC):

    @abstractmethod
    def handle(self, telemetry):
        pass
