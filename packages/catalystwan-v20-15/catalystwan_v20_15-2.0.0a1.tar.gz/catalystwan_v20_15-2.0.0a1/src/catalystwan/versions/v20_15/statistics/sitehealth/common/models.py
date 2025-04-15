# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from typing import Literal

AppsHealth = Literal["fair", "good", "poor"]

DevicesHealth = Literal["fair", "good", "poor"]

SiteHealth = Literal["fair", "good", "poor"]

TunnelsHealth = Literal["fair", "good", "poor"]

HealthParam = Literal["FAIR", "GOOD", "POOR"]

DeviceTypeParam = Literal["all", "controller", "vedge"]


@dataclass
class SiteHealthItem:
    apps_health: AppsHealth  # pytype: disable=annotation-type-mismatch
    apps_usage: int
    devices_health: DevicesHealth  # pytype: disable=annotation-type-mismatch
    site_health: SiteHealth  # pytype: disable=annotation-type-mismatch
    site_id: str
    tunnels_health: TunnelsHealth  # pytype: disable=annotation-type-mismatch
