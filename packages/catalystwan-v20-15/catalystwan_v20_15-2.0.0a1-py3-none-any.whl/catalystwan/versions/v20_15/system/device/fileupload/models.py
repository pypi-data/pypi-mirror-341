# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class FormPostResp:
    activity_list: Optional[str] = _field(default=None, metadata={"alias": "activityList"})
    id: Optional[str] = _field(default=None)
    vedge_list_upload_msg: Optional[str] = _field(
        default=None, metadata={"alias": "vedgeListUploadMsg"}
    )
    vedge_list_upload_status: Optional[str] = _field(
        default=None, metadata={"alias": "vedgeListUploadStatus"}
    )
