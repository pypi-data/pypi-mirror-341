# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class LinkObject:
    href: Optional[str] = _field(default=None)
    rel: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class VersionInformation:
    current_server_version: Optional[str] = _field(
        default=None, metadata={"alias": "currentServerVersion"}
    )
    link: Optional[LinkObject] = _field(default=None)
    supported_versions: Optional[str] = _field(
        default=None, metadata={"alias": "supportedVersions"}
    )


@dataclass
class ConnectResponse:
    """
    Response from ISE ERS version info api
    """

    version_info: Optional[VersionInformation] = _field(
        default=None, metadata={"alias": "VersionInfo"}
    )
