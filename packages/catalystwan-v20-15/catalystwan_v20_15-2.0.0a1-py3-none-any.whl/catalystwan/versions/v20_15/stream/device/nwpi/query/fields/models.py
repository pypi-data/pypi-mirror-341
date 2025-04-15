# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Optional


@dataclass
class QueryFieldsResponsePayloadInner:
    """
    Nwpi Query fields
    """

    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    is_required: Optional[bool] = _field(default=None, metadata={"alias": "isRequired"})
    multi_select: Optional[bool] = _field(default=None, metadata={"alias": "multiSelect"})
    name: Optional[str] = _field(default=None)
    property: Optional[str] = _field(default=None)
    validation: Optional[Any] = _field(default=None)
