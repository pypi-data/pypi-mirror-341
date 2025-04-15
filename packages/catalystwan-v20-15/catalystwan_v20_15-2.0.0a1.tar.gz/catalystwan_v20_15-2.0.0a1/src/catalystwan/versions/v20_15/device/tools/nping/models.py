# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NPingResponse:
    avg_round_trip: Optional[int] = _field(default=None, metadata={"alias": "avgRoundTrip"})
    loss_percentage: Optional[int] = _field(default=None, metadata={"alias": "lossPercentage"})
    max_round_trip: Optional[int] = _field(default=None, metadata={"alias": "maxRoundTrip"})
    min_round_trip: Optional[int] = _field(default=None, metadata={"alias": "minRoundTrip"})
    packets_received: Optional[int] = _field(default=None, metadata={"alias": "packetsReceived"})
    packets_transmitted: Optional[int] = _field(
        default=None, metadata={"alias": "packetsTransmitted"}
    )
    raw_output: Optional[List[str]] = _field(default=None, metadata={"alias": "rawOutput"})


@dataclass
class NPingRequest:
    count: Optional[str] = _field(default=None)
    dest_port: Optional[str] = _field(default=None, metadata={"alias": "destPort"})
    df: Optional[str] = _field(default=None)
    host: Optional[str] = _field(default=None)
    interface_ip: Optional[str] = _field(default=None, metadata={"alias": "interfaceIP"})
    mtu: Optional[str] = _field(default=None)
    probe_type: Optional[str] = _field(default=None, metadata={"alias": "probeType"})
    rapid: Optional[str] = _field(default=None)
    size: Optional[str] = _field(default=None)
    source: Optional[str] = _field(default=None)
    source_port: Optional[str] = _field(default=None, metadata={"alias": "sourcePort"})
    tos: Optional[str] = _field(default=None)
    ttl: Optional[str] = _field(default=None)
    vpn: Optional[str] = _field(default=None)
