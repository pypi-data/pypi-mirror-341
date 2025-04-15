# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class SpeedTestStatusResponse:
    """
    This is valid speedTestStatusResponse
    """

    status: Optional[str] = _field(default=None)


@dataclass
class Uuid:
    """
    This is valid uuid
    """

    uuid: Optional[str] = _field(default=None)
