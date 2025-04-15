# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional, overload

from catalystwan.abc import RequestAdapterInterface


class SegmentBuilder:
    """
    Builds and executes requests for operations under /segment
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Create network segment
        POST /dataservice/segment

        :param payload: Network segment
        :returns: Any
        """
        return self._request_adapter.request("POST", "/dataservice/segment", payload=payload, **kw)

    def put(self, id: str, payload: Any, **kw):
        """
        Edit network segment
        PUT /dataservice/segment/{id}

        :param id: Segment Id
        :param payload: Network segment
        :returns: None
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/segment/{id}", params=params, payload=payload, **kw
        )

    def delete(self, id: str, **kw):
        """
        Delete network segment
        DELETE /dataservice/segment/{id}

        :param id: Segment Id
        :returns: None
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/segment/{id}", params=params, **kw
        )

    @overload
    def get(self, id: str, **kw) -> List[Any]:
        """
        Get network segment
        GET /dataservice/segment/{id}

        :param id: Segment Id
        :returns: List[Any]
        """
        ...

    @overload
    def get(self, **kw) -> List[Any]:
        """
        Get network segments
        GET /dataservice/segment

        :returns: List[Any]
        """
        ...

    def get(self, id: Optional[str] = None, **kw) -> List[Any]:
        # /dataservice/segment/{id}
        if self._request_adapter.param_checker([(id, str)], []):
            params = {
                "id": id,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/segment/{id}", return_type=List[Any], params=params, **kw
            )
        # /dataservice/segment
        if self._request_adapter.param_checker([], [id]):
            return self._request_adapter.request(
                "GET", "/dataservice/segment", return_type=List[Any], **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")
