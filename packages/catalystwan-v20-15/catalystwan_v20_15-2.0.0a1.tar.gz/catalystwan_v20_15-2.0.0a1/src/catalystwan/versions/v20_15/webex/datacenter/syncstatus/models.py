# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class SyncStatusResponse:
    last_synced: Optional[str] = _field(default=None, metadata={"alias": "Last Synced"})
    webex_sync_needed: Optional[bool] = _field(default=None, metadata={"alias": "webexSyncNeeded"})
