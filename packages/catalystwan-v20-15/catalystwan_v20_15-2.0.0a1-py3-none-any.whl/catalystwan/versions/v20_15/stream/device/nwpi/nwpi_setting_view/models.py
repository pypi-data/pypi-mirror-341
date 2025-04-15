# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class NwpiSettingDataPayload:
    """
    Nwpi setting data schema
    """

    peer_site_threshold: Optional[int] = _field(
        default=None, metadata={"alias": "peerSiteThreshold"}
    )
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
