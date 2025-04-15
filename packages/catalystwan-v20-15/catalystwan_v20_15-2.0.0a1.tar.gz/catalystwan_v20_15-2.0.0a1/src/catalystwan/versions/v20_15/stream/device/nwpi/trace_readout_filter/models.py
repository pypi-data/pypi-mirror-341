# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class EventReadoutFilterResponsePayload:
    """
    Event readouts Filter Response schema
    """

    # User Name List
    user_name: Optional[List[str]] = _field(default=None, metadata={"alias": "userName"})
