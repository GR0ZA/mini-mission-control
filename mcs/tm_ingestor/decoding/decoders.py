import struct
from datetime import datetime
from tm_ingestor.domain.models import HousekeepingTM, AttitudeTM, SpacecraftMode
from tm_ingestor.decoding.decoder_base import TelemetryDecoder
from shared.domain.packet_defs import HK_PACKET_ID, ATT_PACKET_ID, HK_FORMAT, ATT_FORMAT


class HousekeepingDecoder(TelemetryDecoder):
    packet_id = HK_PACKET_ID

    def decode(self, payload: bytes) -> HousekeepingTM:
        (
            packet_id,
            seq,
            timestamp_raw,
            battery_mv,
            temp_c10,
            mode_raw
        ) = struct.unpack(HK_FORMAT, payload)

        return HousekeepingTM(
            packet_id=packet_id,
            sequence=seq,
            timestamp=datetime.fromtimestamp(timestamp_raw),
            battery_voltage_v=battery_mv / 1000.0,
            temperature_c=temp_c10 / 10.0,
            mode=SpacecraftMode(mode_raw)
        )


class AttitudeDecoder(TelemetryDecoder):
    packet_id = ATT_PACKET_ID

    def decode(self, payload: bytes) -> AttitudeTM:
        (
            packet_id,
            seq,
            timestamp_raw,
            roll,
            pitch,
            yaw
        ) = struct.unpack(ATT_FORMAT, payload)

        return AttitudeTM(
            packet_id=packet_id,
            sequence=seq,
            timestamp=datetime.fromtimestamp(timestamp_raw),
            roll_deg=roll / 100.0,
            pitch_deg=pitch / 100.0,
            yaw_deg=yaw / 100.0
        )
