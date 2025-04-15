# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class PackagingDistributionData:
    available_cssm: Optional[int] = _field(default=None, metadata={"alias": "availableCssm"})
    license: Optional[str] = _field(default=None)
    used_cssm: Optional[str] = _field(default=None, metadata={"alias": "usedCssm"})
    used_vmanage: Optional[int] = _field(default=None, metadata={"alias": "usedVmanage"})


@dataclass
class PackagingDistribution:
    data: Optional[PackagingDistributionData] = _field(default=None)
