import operator

OPERATORS = {
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
}


class RuleEngine:
    def __init__(self, rules):
        self.rules = [r for r in rules if r.enabled]

    def evaluate(self, telemetry):
        violated = []
        cleared = []

        tm_type = type(telemetry).__name__

        for rule in self.rules:
            if rule.packet_type != tm_type:
                continue

            value = getattr(telemetry, rule.field, None)
            if value is None:
                continue

            if OPERATORS[rule.operator](value, rule.threshold):
                violated.append((rule, value))
            else:
                cleared.append(rule)

        return violated, cleared
