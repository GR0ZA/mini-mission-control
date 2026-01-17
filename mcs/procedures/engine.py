from procedures.procedure_loader import ProcedureLoader
from procedures.executor import ProcedureExecutor


class ProcedureEngine:
    def __init__(self, procedure_file: str):
        loader = ProcedureLoader(procedure_file)
        self.procedures = loader.load()
        self.executor = ProcedureExecutor()

    def on_alert(self, alert):
        for proc in self.procedures:
            trigger = proc.get("trigger", {})
            if trigger.get("alert_id") == alert.rule_id:
                self.executor.execute(proc)
