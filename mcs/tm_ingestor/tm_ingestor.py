import socket
import struct
import binascii

from tm_ingestor.decoding.registry import DECODERS
from tm_ingestor.dispatcher.dispatcher import TelemetryDispatcher
from tm_ingestor.sinks.logging_sink import LoggingSink
from tm_ingestor.sinks.monitoring_sink import MonitoringSink
from tm_ingestor.sinks.archive_sink import ArchiveSink

from shared.domain.packet_defs import (
    CRC_FORMAT,
    CRC_SIZE,
    CRC_INIT,
)


UDP_IP = "0.0.0.0"
UDP_PORT = 5005

HEADER_FORMAT = "!H"

dispatcher = TelemetryDispatcher(
    sinks=[
        LoggingSink(),
        MonitoringSink(),
        ArchiveSink(),
    ]
)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


print(f"TM Ingestor listening on UDP {UDP_PORT}")

while True:
    data, adr = sock.recvfrom(1024)

    packet_id = struct.unpack(HEADER_FORMAT, data[:2])[0]

    if packet_id not in DECODERS:
        print(f"Unknown packet ID {hex(packet_id)}")
        continue

    payload = data[:-CRC_SIZE]
    received_crc = struct.unpack(CRC_FORMAT, data[-CRC_SIZE:])[0]
    calculated_crc = binascii.crc_hqx(payload, CRC_INIT)

    if received_crc != calculated_crc:
        print(
            f"CRC mismatch from {adr}: received {hex(received_crc)}, calculated {hex(calculated_crc)}. Packet discarded."
        )
        continue

    decoder = DECODERS[packet_id]
    tm = decoder.decode(payload)

    dispatcher.dispatch(tm)
