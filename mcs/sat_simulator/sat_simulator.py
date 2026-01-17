import socket
import time
import random
import struct
import binascii
import threading
from dataclasses import dataclass
from enum import IntEnum

from shared.domain.packet_defs import (
    HK_PACKET_ID,
    ATT_PACKET_ID,
    TC_VER_PACKET_ID,
    HK_FORMAT,
    ATT_FORMAT,
    CRC_INIT,
    TC_FORMAT,
    TC_VER_FORMAT,
)
from shared.domain.tc import (
    SpacecraftMode,
    TcCommand,
    TcVerStatus
)
from sat_simulator.spacecraft import SpacecraftState

TC_PORT = 6000

state = SpacecraftState()

TM_IP = "tm-ingestor"
TM_PORT = 5005

tm_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seq = 0


# ===============================
# TM HELPERS
# ===============================

def send_packet(payload: bytes):
    crc = binascii.crc_hqx(payload, CRC_INIT)
    packet = payload + struct.pack("!H", crc)
    tm_sock.sendto(packet, (TM_IP, TM_PORT))


def send_housekeeping():
    global seq
    payload = struct.pack(
        HK_FORMAT,
        HK_PACKET_ID,
        seq,
        int(time.time()),
        state.battery_mv,
        state.temperature_c10,
        state.mode.value
    )
    send_packet(payload)
    print(f"[TM] HK seq={seq} mode={state.mode.name}")


def send_attitude():
    global seq
    payload = struct.pack(
        ATT_FORMAT,
        ATT_PACKET_ID,
        seq,
        int(time.time()),
        state.roll,
        state.pitch,
        state.yaw
    )
    send_packet(payload)
    print(f"[TM] ATT seq={seq}")


def send_tc_verification(tc_seq: int, status: TcVerStatus):
    global seq
    payload = struct.pack(
        TC_VER_FORMAT,
        TC_VER_PACKET_ID,
        seq,
        int(time.time()),
        tc_seq,
        status.value
    )
    send_packet(payload)
    print(f"[TM] TC_VER tc_seq={tc_seq} status={status.name}")


# ===============================
# TC LISTENER
# ===============================

def tc_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", TC_PORT))
    print(f"[SAT] TC listener active on {TC_PORT}")

    while True:
        data, _ = sock.recvfrom(1024)

        payload = data[:-2]
        crc_recv = struct.unpack("!H", data[-2:])[0]
        crc_calc = binascii.crc_hqx(payload, CRC_INIT)

        if crc_recv != crc_calc:
            print("[SAT] TC CRC ERROR")
            continue

        _, tc_seq, _, cmd, param = struct.unpack(TC_FORMAT, payload)

        send_tc_verification(tc_seq, TcVerStatus.ACCEPTED)

        try:
            if TcCommand(cmd) == TcCommand.SET_MODE:
                state.mode = SpacecraftMode(param)
                send_tc_verification(tc_seq, TcVerStatus.EXECUTED)

            elif TcCommand(cmd) == TcCommand.RESET:
                state.mode = SpacecraftMode.SAFE
                state.battery_mv = 3800
                state.temperature_c10 = 250
                send_tc_verification(tc_seq, TcVerStatus.EXECUTED)

            else:
                send_tc_verification(tc_seq, TcVerStatus.FAILED)

        except Exception:
            send_tc_verification(tc_seq, TcVerStatus.FAILED)


# ===============================
# MAIN LOOP
# ===============================

threading.Thread(target=tc_listener, daemon=True).start()

while True:
    state.evolve()

    if random.random() < 0.7:
        send_housekeeping()
    else:
        send_attitude()

    seq = (seq + 1) % 256
    time.sleep(3)
