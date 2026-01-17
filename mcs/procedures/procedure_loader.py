import json


class ProcedureLoader:
    def __init__(self, path: str):
        with open(path) as f:
            self.raw = json.load(f)

    def load(self):
        return self.raw.get("procedures", [])
