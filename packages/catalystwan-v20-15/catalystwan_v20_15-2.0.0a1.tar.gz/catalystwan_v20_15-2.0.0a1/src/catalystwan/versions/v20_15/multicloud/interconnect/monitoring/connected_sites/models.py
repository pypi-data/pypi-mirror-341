# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class InterconnectConnectedSite:
    bfd_sessions: Optional[int] = _field(default=None, metadata={"alias": "bfdSessions"})
    bfd_sessions_up: Optional[int] = _field(default=None, metadata={"alias": "bfdSessionsUp"})
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    last_updated: Optional[int] = _field(default=None, metadata={"alias": "lastUpdated"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    status: Optional[str] = _field(default=None)
    status_bfd: Optional[str] = _field(default=None, metadata={"alias": "statusBfd"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    uuid: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)
