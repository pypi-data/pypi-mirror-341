# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional, overload

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /networkdesign/profile/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, profile_id: str, **kw) -> Any:
        """
        Get device profile configuration status by profile Id
        GET /dataservice/networkdesign/profile/status/{profileId}

        :param profile_id: Device profile Id
        :returns: Any
        """
        ...

    @overload
    def get(self, **kw) -> Any:
        """
        Get device profile configuration status
        GET /dataservice/networkdesign/profile/status

        :returns: Any
        """
        ...

    def get(self, profile_id: Optional[str] = None, **kw) -> Any:
        # /dataservice/networkdesign/profile/status/{profileId}
        if self._request_adapter.param_checker([(profile_id, str)], []):
            logging.warning(
                "Operation: %s is deprecated", "getDeviceProfileConfigStatusByProfileId"
            )
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/networkdesign/profile/status/{profileId}", params=params, **kw
            )
        # /dataservice/networkdesign/profile/status
        if self._request_adapter.param_checker([], [profile_id]):
            logging.warning("Operation: %s is deprecated", "getDeviceProfileConfigStatus")
            return self._request_adapter.request(
                "GET", "/dataservice/networkdesign/profile/status", **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")
