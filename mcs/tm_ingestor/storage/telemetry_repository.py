import sqlite3
import os
from tm_ingestor.domain.models import HousekeepingTM, AttitudeTM


class TelemetryRepository:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv("DB_PATH", "telemetry.db")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_schema()

    def _init_schema(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS housekeeping_tm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            packet_id INTEGER,
            sequence INTEGER,
            timestamp TEXT,
            battery_voltage REAL,
            temperature REAL,
            mode TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS attitude_tm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            packet_id INTEGER,
            sequence INTEGER,
            timestamp TEXT,
            roll REAL,
            pitch REAL,
            yaw REAL
        )
        """)

        self.conn.commit()

    def store(self, telemetry):
        cur = self.conn.cursor()

        if isinstance(telemetry, HousekeepingTM):
            cur.execute("""
            INSERT INTO housekeeping_tm
            VALUES (NULL, ?, ?, ?, ?, ?, ?)
            """, (
                telemetry.packet_id,
                telemetry.sequence,
                telemetry.timestamp.isoformat(),
                telemetry.battery_voltage_v,
                telemetry.temperature_c,
                telemetry.mode.name
            ))

        elif isinstance(telemetry, AttitudeTM):
            cur.execute("""
            INSERT INTO attitude_tm
            VALUES (NULL, ?, ?, ?, ?, ?, ?)
            """, (
                telemetry.packet_id,
                telemetry.sequence,
                telemetry.timestamp.isoformat(),
                telemetry.roll_deg,
                telemetry.pitch_deg,
                telemetry.yaw_deg
            ))

        self.conn.commit()
