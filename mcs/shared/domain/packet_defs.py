import struct
from enum import IntEnum

### TELEMETRY PACKET DEFINITIONS ###

HK_PACKET_ID = 0x0104
ATT_PACKET_ID = 0x0201

# Struct formats
CRC_FORMAT = "!H"
CRC_SIZE = struct.calcsize(CRC_FORMAT)
CRC_INIT = 0xFFFF

# Housekeeping Packet Structure
# ┌──────────┬─────┬──────────┬─────────┬────────┬──────┐
# │ PacketID │ Seq │ Timestamp│ Battery │ Temp   │ Mode │
# │  2 B     │ 1 B │  4 B     │  2 B    │ 2 B    │ 1 B  │
# └──────────┴─────┴──────────┴─────────┴────────┴──────┘
HK_FORMAT = "!H B I H h B"
HK_PACKET_SIZE = struct.calcsize(HK_FORMAT) + CRC_SIZE

# Attitude Packet Structure
# ┌──────────┬─────┬──────────┬─────────┬────────┬──────┐
# │ PacketID │ Seq │ Timestamp│ Roll    │ Pitch  │ Yaw  │
# │  2 B     │ 1 B │  4 B     │ 2 B     │ 2 B    │ 2 B  │
# └──────────┴─────┴──────────┴─────────┴────────┴──────┘
ATT_FORMAT = "!H B I h h h"
ATT_PACKET_SIZE = struct.calcsize(ATT_FORMAT) + CRC_SIZE


### TELECOMMAND PACKET DEFINITIONS ###

TC_PACKET_ID = 0x1001
TC_VER_PACKET_ID = 0x0301

# Telecommand Packet Structure
# ┌──────────┬─────┬──────────┬────────┬────────┐
# │ PacketID │ Seq │ Timestamp│ Command│ Param  │
# │  2 B     │ 1 B │  4 B     │ 1 B    │ 1 B    │
# └──────────┴─────┴──────────┴────────┴────────┘
TC_FORMAT = "!H B I B B"
TC_PACKET_SIZE = struct.calcsize(TC_FORMAT) + CRC_SIZE

# Telecommand Verification Packet Structure
# ┌────────────┬─────┬──────────┬────────┬───────────┐
# │ PacketID   │ Seq │ Timestamp│ TC_Seq │ Status    │
# │  2 B       │ 1 B │  4 B     │ 1 B    │ 1 B       │
# └────────────┴─────┴──────────┴────────┴───────────┘
TC_VER_FORMAT = "!H B I B B"
TC_VER_PACKET_SIZE = struct.calcsize(TC_VER_FORMAT) + CRC_SIZE
