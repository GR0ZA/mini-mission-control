from tm_ingestor.sinks.telemetry_sink import TelemetrySink


class TelemetryDispatcher:
    def __init__(self, sinks: list[TelemetrySink]):
        self.sinks = sinks

    def dispatch(self, telemetry):
        for sink in self.sinks:
            try:
                sink.handle(telemetry)
            except Exception as e:
                print(f"[DISPATCH ERROR] {e}")
