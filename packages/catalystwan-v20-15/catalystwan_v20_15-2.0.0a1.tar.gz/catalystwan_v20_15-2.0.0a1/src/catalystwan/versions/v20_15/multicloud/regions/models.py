# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

CloudTypeParam = Literal["AWS", "AWS_GOVCLOUD", "AZURE", "AZURE_GOVCLOUD", "GCP"]


@dataclass
class GetRegions:
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    region_list: Optional[str] = _field(default=None, metadata={"alias": "regionList"})
