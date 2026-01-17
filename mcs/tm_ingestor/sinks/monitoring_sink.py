import json
from tm_ingestor.sinks.telemetry_sink import TelemetrySink
from tm_ingestor.monitoring.monitoring_rule import MonitoringRule
from tm_ingestor.monitoring.rule_engine import RuleEngine
from tm_ingestor.alerts.alert_manager import AlertManager
from shared.storage.alert_repository import AlertRepository


class MonitoringSink(TelemetrySink):
    def __init__(self, rule_file="tm_ingestor/monitoring/rules.json"):
        with open(rule_file) as f:
            raw_rules = json.load(f)

        rules = [MonitoringRule(**r) for r in raw_rules]
        self.engine = RuleEngine(rules)
        self.alert_manager = AlertManager(AlertRepository())

    def handle(self, telemetry):
        violated, cleared = self.engine.evaluate(telemetry)

        for rule, value in violated:
            self.alert_manager.handle_violation(rule, telemetry, value)

        for rule in cleared:
            self.alert_manager.handle_clearance(rule)
