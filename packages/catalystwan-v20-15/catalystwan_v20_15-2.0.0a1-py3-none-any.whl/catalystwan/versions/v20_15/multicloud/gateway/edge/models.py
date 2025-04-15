# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

EdgeTypeParam = Literal["EQUINIX", "MEGAPORT"]

ValueType = Literal["ARRAY", "FALSE", "NULL", "NUMBER", "OBJECT", "STRING", "TRUE"]


@dataclass
class UpdateIcgwPutRequest:
    empty: Optional[bool] = _field(default=None)
    value_type: Optional[ValueType] = _field(default=None, metadata={"alias": "valueType"})
