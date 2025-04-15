# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class MdpconfigBuilder:
    """
    Builds and executes requests for operations under /mdp/policies/mdpconfig
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: Any, **kw) -> Any:
        """
        Add internal policy from vmanage
        PUT /dataservice/mdp/policies/mdpconfig

        :param payload: addInternalPolicy
        :returns: Any
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/mdp/policies/mdpconfig", payload=payload, **kw
        )

    def get(self, device_id: str, **kw) -> List[Any]:
        """
        Retrieve MDP ConfigObject
        GET /dataservice/mdp/policies/mdpconfig/{deviceId}

        :param device_id: Device id
        :returns: List[Any]
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/mdp/policies/mdpconfig/{deviceId}",
            return_type=List[Any],
            params=params,
            **kw,
        )
