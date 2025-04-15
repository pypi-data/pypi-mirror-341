# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Optional


@dataclass
class TraceFinFlowTimeRangeResponsePayloadInner:
    """
    Fin Flow schema for GET response
    """

    data: Optional[Any] = _field(default=None)
    data_received_timestamp: Optional[int] = _field(
        default=None, metadata={"alias": "data.received_timestamp"}
    )
    entry_time: Optional[int] = _field(default=None)
    tenant: Optional[str] = _field(default=None)
    trace_id: Optional[int] = _field(default=None, metadata={"alias": "trace-id"})
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})
