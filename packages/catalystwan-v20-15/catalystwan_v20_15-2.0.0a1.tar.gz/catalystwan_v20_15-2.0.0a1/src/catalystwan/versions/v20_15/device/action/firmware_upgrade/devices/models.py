# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class ProcessGetFirmwareRemoteImageReq:
    description: Optional[str] = _field(default=None)
    file_path: Optional[str] = _field(default=None, metadata={"alias": "filePath"})
    remote_server_id: Optional[str] = _field(default=None, metadata={"alias": "remoteServerId"})
    version_id: Optional[str] = _field(default=None, metadata={"alias": "versionId"})
