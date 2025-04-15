# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class EventName:
    """
    This is valid eventName
    """

    event_name: Optional[str] = _field(default=None, metadata={"alias": "eventName"})
