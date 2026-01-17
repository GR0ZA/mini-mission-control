from tm_ingestor.decoding.decoders import HousekeepingDecoder, AttitudeDecoder

DECODERS = {
    HousekeepingDecoder.packet_id: HousekeepingDecoder(),
    AttitudeDecoder.packet_id: AttitudeDecoder(),
}
