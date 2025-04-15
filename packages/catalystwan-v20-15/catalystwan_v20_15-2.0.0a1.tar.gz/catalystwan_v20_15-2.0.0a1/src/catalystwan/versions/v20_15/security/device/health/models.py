# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass


@dataclass
class SecurityDeviceHealth:
    amp_cloud_reachability: str
    ips_cloud_reachability: str
    ips_last_upload: int
    ips_package_version: str
    utd_container_health: str
