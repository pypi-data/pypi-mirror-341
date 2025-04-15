# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class FindSoftwareVersionData:
    version: Optional[str] = _field(default=None)


@dataclass
class FindSoftwareVersion:
    data: Optional[List[FindSoftwareVersionData]] = _field(default=None)
