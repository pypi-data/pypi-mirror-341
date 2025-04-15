# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class Hops:
    error_info: Optional[str] = _field(default=None, metadata={"alias": "errorInfo"})
    hop_name: Optional[str] = _field(default=None, metadata={"alias": "hopName"})
    hop_number: Optional[str] = _field(default=None, metadata={"alias": "hopNumber"})
    ip_address: Optional[str] = _field(default=None, metadata={"alias": "ipAddress"})
    mean_latency: Optional[str] = _field(default=None, metadata={"alias": "meanLatency"})


@dataclass
class TracerouteResponse:
    nexthops: Optional[List[Hops]] = _field(default=None)
    raw_output: Optional[List[str]] = _field(default=None, metadata={"alias": "rawOutput"})


@dataclass
class TracerouteRequest:
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "deviceIp"})
    host: Optional[str] = _field(default=None)
    interface: Optional[str] = _field(default=None)
    interface_ip: Optional[str] = _field(default=None, metadata={"alias": "interfaceIP"})
    size: Optional[str] = _field(default=None)
    vpn: Optional[str] = _field(default=None)
