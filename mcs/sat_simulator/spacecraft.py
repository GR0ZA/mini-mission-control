import random
from dataclasses import dataclass
from shared.domain.tc import (
    SpacecraftMode,
)


@dataclass
class SpacecraftState:
    mode: SpacecraftMode = SpacecraftMode.NOMINAL
    battery_mv: int = 3800
    temperature_c10: int = 250
    roll: int = 0
    pitch: int = 0
    yaw: int = 0

    def evolve(self):
        if self.mode == SpacecraftMode.NOMINAL:
            self.battery_mv -= random.randint(0, 2)
            self.temperature_c10 += random.randint(-2, 3)
        else:
            self.battery_mv -= random.randint(0, 1)
            self.temperature_c10 += random.randint(-1, 1)

        self.battery_mv = max(3000, min(4200, self.battery_mv))
        self.temperature_c10 = max(150, min(600, self.temperature_c10))

        self.roll = random.randint(-18000, 18000)
        self.pitch = random.randint(-9000, 9000)
        self.yaw = random.randint(-18000, 18000)
