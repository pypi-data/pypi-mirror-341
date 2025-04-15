# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SshKeyList


class SshkeysBuilder:
    """
    Builds and executes requests for operations under /multicloud/sshkeys
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_type: str, account_id: str, cloud_region: str, **kw) -> List[SshKeyList]:
        """
        Get ssh keyList for cloud type
        GET /dataservice/multicloud/sshkeys

        :param cloud_type: Cloud type
        :param account_id: Account id
        :param cloud_region: Cloud region
        :returns: List[SshKeyList]
        """
        params = {
            "cloudType": cloud_type,
            "accountId": account_id,
            "cloudRegion": cloud_region,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/sshkeys",
            return_type=List[SshKeyList],
            params=params,
            **kw,
        )
