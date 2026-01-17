from fastapi import FastAPI, APIRouter
from shared.storage.alert_repository import AlertRepository
from api.schemas import AlertOut
from datetime import datetime
from tc_uplink.tc_builder import TcBuilder
from tc_uplink.tc_uplink import TcUplink
from shared.domain.tc import TcCommand, SpacecraftMode


app = FastAPI(title="Mission Control Alert API")

router = APIRouter()
repo = AlertRepository()

builder = TcBuilder()
uplink = TcUplink()


def row_to_alert(row):
    return AlertOut(
        id=row[0],
        rule_id=row[1],
        severity=row[2],
        packet_type=row[3],
        field=row[4],
        message=row[5],
        first_seen=datetime.fromisoformat(row[6]),
        last_seen=datetime.fromisoformat(row[7]),
        status=row[8],
    )


@app.get("/alerts", response_model=list[AlertOut])
def list_active_alerts():
    rows = repo.list_alerts(active_only=True)
    return [row_to_alert(r) for r in rows]


@app.get("/alerts/history", response_model=list[AlertOut])
def list_all_alerts():
    rows = repo.list_alerts(active_only=False)
    return [row_to_alert(r) for r in rows]


@app.post("/alerts/{alert_id}/ack")
def acknowledge_alert(alert_id: int):
    repo.acknowledge(alert_id)
    return {"status": "acknowledged", "alert_id": alert_id}


@router.post("/commands/set-mode")
def set_mode(mode: SpacecraftMode):
    packet = builder.build(TcCommand.SET_MODE, mode)
    uplink.send(packet)
    return {"status": "TC_SENT", "command": "SET_MODE", "mode": mode.name}
