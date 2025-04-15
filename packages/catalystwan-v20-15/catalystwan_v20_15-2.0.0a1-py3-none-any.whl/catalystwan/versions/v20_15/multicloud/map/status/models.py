# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class MapStatusMapped:
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    dest_id: Optional[str] = _field(default=None, metadata={"alias": "destId"})
    dest_region: Optional[str] = _field(default=None, metadata={"alias": "destRegion"})
    dest_type: Optional[str] = _field(default=None, metadata={"alias": "destType"})
    source_region: Optional[str] = _field(default=None, metadata={"alias": "sourceRegion"})
    source_tag: Optional[str] = _field(default=None, metadata={"alias": "sourceTag"})
    src_id: Optional[str] = _field(default=None, metadata={"alias": "srcId"})
    src_type: Optional[str] = _field(default=None, metadata={"alias": "srcType"})
    tunnel_id: Optional[str] = _field(default=None, metadata={"alias": "tunnelId"})


@dataclass
class MapStatus:
    dest_id: Optional[str] = _field(default=None, metadata={"alias": "destId"})
    dest_type: Optional[str] = _field(default=None, metadata={"alias": "destType"})
    mapped: Optional[List[MapStatusMapped]] = _field(default=None)
    outstanding_mapping: Optional[str] = _field(
        default=None, metadata={"alias": "outstandingMapping"}
    )
    src_id: Optional[str] = _field(default=None, metadata={"alias": "srcId"})
    src_type: Optional[str] = _field(default=None, metadata={"alias": "srcType"})
    unmapped: Optional[str] = _field(default=None)
