from tm_ingestor.sinks.telemetry_sink import TelemetrySink


class LoggingSink(TelemetrySink):
    def handle(self, telemetry):
        print(f"[LOG] {telemetry}")
