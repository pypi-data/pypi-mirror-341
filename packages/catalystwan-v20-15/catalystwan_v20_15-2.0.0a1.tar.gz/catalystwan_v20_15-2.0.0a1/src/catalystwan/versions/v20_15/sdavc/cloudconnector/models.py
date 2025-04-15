# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

ValueType = Literal["ARRAY", "FALSE", "NULL", "NUMBER", "OBJECT", "STRING", "TRUE"]


@dataclass
class DisableCloudConnectorPutRequest:
    empty: Optional[bool] = _field(default=None)
    value_type: Optional[ValueType] = _field(default=None, metadata={"alias": "valueType"})


@dataclass
class EnableCloudConnectorPostRequest:
    empty: Optional[bool] = _field(default=None)
    value_type: Optional[ValueType] = _field(default=None, metadata={"alias": "valueType"})
