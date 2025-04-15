# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam, GetMapResponse, PostMapRequest, Taskid

if TYPE_CHECKING:
    from .defaults.defaults_builder import DefaultsBuilder
    from .status.status_builder import StatusBuilder
    from .summary.summary_builder import SummaryBuilder
    from .tags.tags_builder import TagsBuilder
    from .vpns.vpns_builder import VpnsBuilder


class MapBuilder:
    """
    Builds and executes requests for operations under /multicloud/map
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_type: CloudTypeParam, **kw) -> List[GetMapResponse]:
        """
        Get Mapping details for cloudType
        GET /dataservice/multicloud/map

        :param cloud_type: Cloud type
        :returns: List[GetMapResponse]
        """
        params = {
            "cloudType": cloud_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/map",
            return_type=List[GetMapResponse],
            params=params,
            **kw,
        )

    def post(self, payload: PostMapRequest, **kw) -> Taskid:
        """
        Enable Mapping for cloudType
        POST /dataservice/multicloud/map

        :param payload: Payloads for enable mapping
        :returns: Taskid
        """
        return self._request_adapter.request(
            "POST", "/dataservice/multicloud/map", return_type=Taskid, payload=payload, **kw
        )

    @property
    def defaults(self) -> DefaultsBuilder:
        """
        The defaults property
        """
        from .defaults.defaults_builder import DefaultsBuilder

        return DefaultsBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)

    @property
    def tags(self) -> TagsBuilder:
        """
        The tags property
        """
        from .tags.tags_builder import TagsBuilder

        return TagsBuilder(self._request_adapter)

    @property
    def vpns(self) -> VpnsBuilder:
        """
        The vpns property
        """
        from .vpns.vpns_builder import VpnsBuilder

        return VpnsBuilder(self._request_adapter)
