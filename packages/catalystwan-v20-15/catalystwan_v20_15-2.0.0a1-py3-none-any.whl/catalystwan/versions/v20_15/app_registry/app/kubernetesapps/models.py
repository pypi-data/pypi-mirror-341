# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DiscoveredServices:
    cluster_name: Optional[str] = _field(default=None, metadata={"alias": "clusterName"})
    ip: Optional[List[str]] = _field(default=None)
    name: Optional[str] = _field(default=None)
    namespace: Optional[str] = _field(default=None)
    port: Optional[List[str]] = _field(default=None)
    protocol: Optional[str] = _field(default=None)
    server_name: Optional[List[str]] = _field(default=None, metadata={"alias": "serverName"})
