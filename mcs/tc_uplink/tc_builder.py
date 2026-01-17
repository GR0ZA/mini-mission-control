
import struct
import time
import binascii
from shared.domain.packet_defs import TC_FORMAT, TC_PACKET_ID
from shared.domain.tc import TcCommand


class TcBuilder:
    def __init__(self):
        self.seq = 0

    def build(self, command: TcCommand, param: int) -> bytes:
        payload = struct.pack(
            TC_FORMAT,
            TC_PACKET_ID,
            self.seq,
            int(time.time()),
            command,
            param
        )

        crc = binascii.crc_hqx(payload, 0xFFFF)
        packet = payload + struct.pack("!H", crc)

        self.seq = (self.seq + 1) % 256
        return packet
