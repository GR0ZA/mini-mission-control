from tm_ingestor.sinks.telemetry_sink import TelemetrySink
from tm_ingestor.storage.telemetry_repository import TelemetryRepository


class ArchiveSink(TelemetrySink):
    def __init__(self):
        self.repository = TelemetryRepository()

    def handle(self, telemetry):
        self.repository.store(telemetry)
