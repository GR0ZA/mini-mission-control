import sqlite3
from datetime import datetime, timezone
from shared.domain.alert import Alert
import os


class AlertRepository:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv("DB_PATH", "telemetry.db")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_id TEXT,
            severity TEXT,
            packet_type TEXT,
            field TEXT,
            message TEXT,
            first_seen TEXT,
            last_seen TEXT,
            status TEXT
        )
        """)
        self.conn.commit()

    def list_alerts(self, active_only=True):
        cur = self.conn.cursor()
        if active_only:
            cur.execute("SELECT * FROM alerts WHERE status!='CLEARED'")
        else:
            cur.execute("SELECT * FROM alerts")
        return cur.fetchall()

    def find_active(self, rule_id):
        cur = self.conn.execute(
            "SELECT * FROM alerts WHERE rule_id=? AND status!='CLEARED'",
            (rule_id,)
        )
        return cur.fetchone()

    def insert(self, alert: Alert):
        cur = self.conn.execute("""
        INSERT INTO alerts
        (rule_id, severity, packet_type, field, message, first_seen, last_seen, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alert.rule_id,
            alert.severity,
            alert.packet_type,
            alert.field,
            alert.message,
            alert.first_seen.isoformat(),
            alert.last_seen.isoformat(),
            alert.status.value
        ))
        self.conn.commit()
        return cur.lastrowid

    def update_last_seen(self, alert_id):
        self.conn.execute(
            "UPDATE alerts SET last_seen=? WHERE id=?",
            (datetime.now(timezone.utc).isoformat(), alert_id)
        )
        self.conn.commit()

    def acknowledge(self, alert_id):
        self.conn.execute(
            "UPDATE alerts SET status='ACK' WHERE id=?",
            (alert_id,)
        )
        self.conn.commit()

    def clear(self, alert_id):
        self.conn.execute(
            "UPDATE alerts SET status='CLEARED' WHERE id=?",
            (alert_id,)
        )
        self.conn.commit()
