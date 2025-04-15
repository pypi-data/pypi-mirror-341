# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class Field:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    display: Optional[str] = _field(default=None)
    property: Optional[str] = _field(default=None)
