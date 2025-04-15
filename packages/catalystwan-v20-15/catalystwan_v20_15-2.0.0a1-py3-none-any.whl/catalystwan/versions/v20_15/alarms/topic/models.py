# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class AlarmTopic:
    device_ip: Optional[str] = _field(default=None, metadata={"alias": "device-ip"})
    server_ip: Optional[str] = _field(default=None, metadata={"alias": "server-ip"})
    topic: Optional[str] = _field(default=None)
