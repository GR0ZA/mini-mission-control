from datetime import datetime, timezone

from shared.domain.alert import Alert, AlertStatus
from procedures.engine import ProcedureEngine


class AlertManager:
    def __init__(self, repository):
        self.repository = repository
        self.procedure_engine = ProcedureEngine(
            "procedures/procedures.json"
        )

    def handle_violation(self, rule, telemetry, value):
        existing_alert = self.repository.find_active(rule.id)
        now = datetime.now(timezone.utc)

        if existing_alert:
            alert_id = existing_alert[0]
            self.repository.update_last_seen(alert_id)
            return

        alert = Alert(
            id=None,
            rule_id=rule.id,
            severity=rule.severity,
            packet_type=rule.packet_type,
            field=rule.field,
            message=(
                f"{rule.field} {rule.operator} {rule.threshold} "
                f"(value={value})"
            ),
            first_seen=now,
            last_seen=now,
            status=AlertStatus.NEW
        )

        self.repository.insert(alert)
        self.procedure_engine.on_alert(alert)

    def handle_clearance(self, rule):
        existing_alert = self.repository.find_active(rule.id)

        if existing_alert:
            alert_id = existing_alert[0]
            self.repository.clear(alert_id)
