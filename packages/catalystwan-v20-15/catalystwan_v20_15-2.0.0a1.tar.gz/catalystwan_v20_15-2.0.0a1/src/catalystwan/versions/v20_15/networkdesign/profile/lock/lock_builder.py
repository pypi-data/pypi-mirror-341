# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class LockBuilder:
    """
    Builds and executes requests for operations under /networkdesign/profile/lock
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, profile_id: str, **kw) -> Any:
        """
        Get the service profile config for a given device profile id
        POST /dataservice/networkdesign/profile/lock/{profileId}

        :param profile_id: Device profile Id
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "acquireAttachLock")
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/networkdesign/profile/lock/{profileId}", params=params, **kw
        )
