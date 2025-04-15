# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetSdroutingFeatureProfilesGetResponse

if TYPE_CHECKING:
    from .cli.cli_builder import CliBuilder
    from .embedded_security.embedded_security_builder import EmbeddedSecurityBuilder
    from .other.other_builder import OtherBuilder
    from .service.service_builder import ServiceBuilder
    from .sse.sse_builder import SseBuilder
    from .system.system_builder import SystemBuilder
    from .transport.transport_builder import TransportBuilder


class SdRoutingBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetSdroutingFeatureProfilesGetResponse]:
        """
        Get all SD-Routing Feature Profiles
        GET /dataservice/v1/feature-profile/sd-routing

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetSdroutingFeatureProfilesGetResponse]
        """
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sd-routing",
            return_type=List[GetSdroutingFeatureProfilesGetResponse],
            params=params,
            **kw,
        )

    @property
    def cli(self) -> CliBuilder:
        """
        The cli property
        """
        from .cli.cli_builder import CliBuilder

        return CliBuilder(self._request_adapter)

    @property
    def embedded_security(self) -> EmbeddedSecurityBuilder:
        """
        The embedded-security property
        """
        from .embedded_security.embedded_security_builder import EmbeddedSecurityBuilder

        return EmbeddedSecurityBuilder(self._request_adapter)

    @property
    def other(self) -> OtherBuilder:
        """
        The other property
        """
        from .other.other_builder import OtherBuilder

        return OtherBuilder(self._request_adapter)

    @property
    def service(self) -> ServiceBuilder:
        """
        The service property
        """
        from .service.service_builder import ServiceBuilder

        return ServiceBuilder(self._request_adapter)

    @property
    def sse(self) -> SseBuilder:
        """
        The sse property
        """
        from .sse.sse_builder import SseBuilder

        return SseBuilder(self._request_adapter)

    @property
    def system(self) -> SystemBuilder:
        """
        The system property
        """
        from .system.system_builder import SystemBuilder

        return SystemBuilder(self._request_adapter)

    @property
    def transport(self) -> TransportBuilder:
        """
        The transport property
        """
        from .transport.transport_builder import TransportBuilder

        return TransportBuilder(self._request_adapter)
