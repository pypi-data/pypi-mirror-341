# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

Method = Literal["DELETE", "GET", "POST", "PUT"]


@dataclass
class BatchFlowData:
    """
    payload for a REST API
    """

    # HTTP Method
    method: Optional[Method] = _field(default=None)
    # JSON Payload for a REST API call
    payload: Optional[Any] = _field(default=None)
    uri: Optional[str] = _field(default=None)


@dataclass
class BatchFlow:
    """
    Input to multiple REST API calls
    """

    # payload for a REST API
    data: List[BatchFlowData]
