# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class VsmartSyncResponse:
    """
    Response for a vsmart sync with the task id for the push from vManage to vSmarts
    """

    id: Optional[str] = _field(default=None)
