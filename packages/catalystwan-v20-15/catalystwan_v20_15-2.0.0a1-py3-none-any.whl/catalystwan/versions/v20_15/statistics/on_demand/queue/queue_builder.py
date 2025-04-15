# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .properties.properties_builder import PropertiesBuilder


class QueueBuilder:
    """
    Builds and executes requests for operations under /statistics/on-demand/queue
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        gets current on-demand queue entries
        GET /dataservice/statistics/on-demand/queue

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/statistics/on-demand/queue", **kw)

    def post(self, payload: Any, **kw) -> Any:
        """
        Create on-demand troubleshooting queue entry
        POST /dataservice/statistics/on-demand/queue

        :param payload: On-demand queue entry
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/statistics/on-demand/queue", payload=payload, **kw
        )

    def put(self, entry_id: str, payload: Any, **kw) -> Any:
        """
        Updates on-demand troubleshooting queue entry
        PUT /dataservice/statistics/on-demand/queue/{entryId}

        :param entry_id: Entry Id
        :param payload: On-demand queue entry
        :returns: Any
        """
        params = {
            "entryId": entry_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/statistics/on-demand/queue/{entryId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, entry_id: str, **kw):
        """
        removes on-demand queue entry
        DELETE /dataservice/statistics/on-demand/queue/{entryId}

        :param entry_id: Entry Id
        :returns: None
        """
        params = {
            "entryId": entry_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/statistics/on-demand/queue/{entryId}", params=params, **kw
        )

    @property
    def properties(self) -> PropertiesBuilder:
        """
        The properties property
        """
        from .properties.properties_builder import PropertiesBuilder

        return PropertiesBuilder(self._request_adapter)
