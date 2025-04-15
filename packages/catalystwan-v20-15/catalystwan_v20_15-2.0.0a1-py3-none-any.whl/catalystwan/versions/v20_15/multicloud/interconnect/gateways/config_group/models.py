# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal

InterconnectTypeParam = Literal["EQUINIX", "MEGAPORT"]


@dataclass
class GatewaysConfiggroupBody:
    config_group_name: str = _field(metadata={"alias": "configGroupName"})
