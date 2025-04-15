# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

CloudTypeParam = Literal["AWS", "AWS_GOVCLOUD", "AZURE", "AZURE_GOVCLOUD", "GCP"]


@dataclass
class CloudGatewayListResponse:
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    cloud_gateway_id: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayId"})
    cloud_gateway_name: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayName"})
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    custom_settings: Optional[bool] = _field(default=None, metadata={"alias": "customSettings"})
    description: Optional[str] = _field(default=None)
    region: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)
