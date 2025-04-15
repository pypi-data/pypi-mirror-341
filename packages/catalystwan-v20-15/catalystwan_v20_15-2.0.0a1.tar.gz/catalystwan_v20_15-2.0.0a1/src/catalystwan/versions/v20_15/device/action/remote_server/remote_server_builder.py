# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional, overload

from catalystwan.abc import RequestAdapterInterface


class RemoteServerBuilder:
    """
    Builds and executes requests for operations under /device/action/remote-server
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Add a new remote server entry.
        POST /dataservice/device/action/remote-server

        :param payload: Request body for Add a new remote server entry.
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/remote-server", payload=payload, **kw
        )

    def put(self, id: str, payload: str, **kw) -> Any:
        """
        Update remote server for the specified ID
        PUT /dataservice/device/action/remote-server/{id}

        :param id: Id
        :param payload: Payload
        :returns: Any
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/device/action/remote-server/{id}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, id: str, payload: Optional[Any] = None, **kw):
        """
        Delete remote server for the specified ID
        DELETE /dataservice/device/action/remote-server/{id}

        :param id: remoteServerId
        :param payload: Request body for Add a new remote server entry.
        :returns: None
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/device/action/remote-server/{id}",
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(self, id: str, **kw) -> Any:
        """
        Get remote server for the specified ID
        GET /dataservice/device/action/remote-server/{id}

        :param id: Id
        :returns: Any
        """
        ...

    @overload
    def get(self, **kw) -> Any:
        """
        Get list of remote servers
        GET /dataservice/device/action/remote-server

        :returns: Any
        """
        ...

    def get(self, id: Optional[str] = None, **kw) -> Any:
        # /dataservice/device/action/remote-server/{id}
        if self._request_adapter.param_checker([(id, str)], []):
            params = {
                "id": id,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/device/action/remote-server/{id}", params=params, **kw
            )
        # /dataservice/device/action/remote-server
        if self._request_adapter.param_checker([], [id]):
            return self._request_adapter.request(
                "GET", "/dataservice/device/action/remote-server", **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")
