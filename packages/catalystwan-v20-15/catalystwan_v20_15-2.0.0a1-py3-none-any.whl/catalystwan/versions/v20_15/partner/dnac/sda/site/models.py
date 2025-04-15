# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class PartnerSite:
    partner_id: Optional[str] = _field(default=None, metadata={"alias": "partnerId"})
    sites: Optional[List[str]] = _field(default=None)


@dataclass
class VpnListResHeader:
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})


@dataclass
class SdaSitesRes:
    data: Optional[List[PartnerSite]] = _field(default=None)
    header: Optional[VpnListResHeader] = _field(default=None)
