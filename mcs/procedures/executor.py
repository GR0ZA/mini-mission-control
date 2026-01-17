import time
from tc_uplink.tc_builder import TcBuilder
from tc_uplink.tc_uplink import TcUplink
from shared.domain.tc import SpacecraftMode, TcCommand


class ProcedureExecutor:
    def __init__(self):
        self.tc_builder = TcBuilder()
        self.tc_uplink = TcUplink()

    def execute(self, procedure: dict):
        print(f"[PROC] Executing procedure {procedure['id']}")

        for step in procedure["steps"]:
            if "send_tc" in step:
                cmd = step["send_tc"]["command"]
                param = step["send_tc"]["param"]

                packet = self.tc_builder.build(
                    TcCommand[cmd],
                    SpacecraftMode[param]
                )
                self.tc_uplink.send(packet)
                print(f"[PROC] TC sent: {cmd} {param}")

            elif "wait" in step:
                seconds = step["wait"]
                print(f"[PROC] Waiting {seconds}s")
                time.sleep(seconds)

            elif "verify" in step:
                # Placerholder: real verification is via TM/TC verification
                print("[PROC] Verification step (implicit via TC_VER TM)")

        print(f"[PROC] Procedure {procedure['id']} completed")
