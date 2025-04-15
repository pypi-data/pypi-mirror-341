# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import LocalBackupInfo


class BackupinfoBuilder:
    """
    Builds and executes requests for operations under /backup/backupinfo
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(
        self, task_id: Optional[str] = None, backup_info_id: Optional[str] = None, **kw
    ) -> Any:
        """
        Delete all or a specific backup file stored in vManage
        DELETE /dataservice/backup/backupinfo

        :param task_id: Task id
        :param backup_info_id: Backup info id
        :returns: Any
        """
        params = {
            "taskId": task_id,
            "backupInfoId": backup_info_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/backup/backupinfo", params=params, **kw
        )

    def get(self, local_backup_info_id: str, **kw) -> LocalBackupInfo:
        """
        Get a localBackupInfo record by localBackupInfoId
        GET /dataservice/backup/backupinfo/{localBackupInfoId}

        :param local_backup_info_id: Local backup info id
        :returns: LocalBackupInfo
        """
        params = {
            "localBackupInfoId": local_backup_info_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/backup/backupinfo/{localBackupInfoId}",
            return_type=LocalBackupInfo,
            params=params,
            **kw,
        )
