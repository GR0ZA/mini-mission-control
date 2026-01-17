from enum import IntEnum


class TcCommand(IntEnum):
    SET_MODE = 1
    RESET = 2


class SpacecraftMode(IntEnum):
    SAFE = 0
    NOMINAL = 1


class TcVerStatus:
    ACCEPTED = 0
    EXECUTED = 1
    FAILED = 2
