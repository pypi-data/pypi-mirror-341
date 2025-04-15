# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class MigrateTenantModel:
    desc: Optional[str] = _field(default=None)
    is_destination_overlay_mt: Optional[bool] = _field(
        default=None, metadata={"alias": "isDestinationOverlayMT"}
    )
    migration_key: Optional[str] = _field(default=None, metadata={"alias": "migrationKey"})
    name: Optional[str] = _field(default=None)
    org_name: Optional[str] = _field(default=None, metadata={"alias": "orgName"})
    sub_domain: Optional[str] = _field(default=None, metadata={"alias": "subDomain"})
    wan_edge_forecast: Optional[str] = _field(default=None, metadata={"alias": "wanEdgeForecast"})
