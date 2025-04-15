# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import IseServer

if TYPE_CHECKING:
    from .iseandpxgrid.iseandpxgrid_builder import IseandpxgridBuilder
    from .pxgrid.pxgrid_builder import PxgridBuilder
    from .vsmart.vsmart_builder import VsmartBuilder


class CredentialsBuilder:
    """
    Builds and executes requests for operations under /ise/credentials
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> IseServer:
        """
        Get Ise server credentials
        GET /dataservice/ise/credentials

        :returns: IseServer
        """
        return self._request_adapter.request(
            "GET", "/dataservice/ise/credentials", return_type=IseServer, **kw
        )

    def put(self, payload: IseServer, **kw) -> bool:
        """
        update Ise server credentials
        PUT /dataservice/ise/credentials

        :param payload: Ise Server with possibly new values for properties
        :returns: bool
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/ise/credentials", return_type=bool, payload=payload, **kw
        )

    def post(self, payload: IseServer, **kw) -> bool:
        """
        Add Ise server credentials
        POST /dataservice/ise/credentials

        :param payload: Ise Server
        :returns: bool
        """
        return self._request_adapter.request(
            "POST", "/dataservice/ise/credentials", return_type=bool, payload=payload, **kw
        )

    @property
    def iseandpxgrid(self) -> IseandpxgridBuilder:
        """
        The iseandpxgrid property
        """
        from .iseandpxgrid.iseandpxgrid_builder import IseandpxgridBuilder

        return IseandpxgridBuilder(self._request_adapter)

    @property
    def pxgrid(self) -> PxgridBuilder:
        """
        The pxgrid property
        """
        from .pxgrid.pxgrid_builder import PxgridBuilder

        return PxgridBuilder(self._request_adapter)

    @property
    def vsmart(self) -> VsmartBuilder:
        """
        The vsmart property
        """
        from .vsmart.vsmart_builder import VsmartBuilder

        return VsmartBuilder(self._request_adapter)
