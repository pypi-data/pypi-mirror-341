# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class InterconnectServiceSwVersion:
    # Service Software Version Image Name
    image_name: Optional[str] = _field(default=None, metadata={"alias": "imageName"})
    # Service Software Version
    version: Optional[str] = _field(default=None)


@dataclass
class InterconnectServiceTypes:
    # Name of the service package
    name: Optional[str] = _field(default=None)
    # provider assigned service package code
    package_code: Optional[str] = _field(default=None, metadata={"alias": "packageCode"})
    service_sw_version: Optional[List[InterconnectServiceSwVersion]] = _field(
        default=None, metadata={"alias": "serviceSwVersion"}
    )


@dataclass
class InlineResponse20015:
    sw_packages: Optional[List[InterconnectServiceTypes]] = _field(
        default=None, metadata={"alias": "swPackages"}
    )
