# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class QoSQueryFieldsRespFieldData:
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class QueryFieldsOption:
    enabled_date_fields: Optional[bool] = _field(
        default=None, metadata={"alias": "enabledDateFields"}
    )
    key: Optional[str] = _field(default=None)
    number: Optional[str] = _field(default=None)
    value: Optional[str] = _field(default=None)


@dataclass
class QoSQueryFieldsResp:
    data_type: Optional[str] = _field(default=None, metadata={"alias": "dataType"})
    field_data: Optional[QoSQueryFieldsRespFieldData] = _field(
        default=None, metadata={"alias": "fieldData"}
    )
    is_required: Optional[bool] = _field(default=None, metadata={"alias": "isRequired"})
    name: Optional[str] = _field(default=None)
    options: Optional[List[QueryFieldsOption]] = _field(default=None)
    property: Optional[str] = _field(default=None)
