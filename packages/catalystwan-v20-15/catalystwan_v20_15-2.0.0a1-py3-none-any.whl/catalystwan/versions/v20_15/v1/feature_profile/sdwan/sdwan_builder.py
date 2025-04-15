# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetSdwanFeatureProfileBySdwanFamilyGetResponse

if TYPE_CHECKING:
    from .application_priority.application_priority_builder import ApplicationPriorityBuilder
    from .cli.cli_builder import CliBuilder
    from .dns_security.dns_security_builder import DnsSecurityBuilder
    from .embedded_security.embedded_security_builder import EmbeddedSecurityBuilder
    from .other.other_builder import OtherBuilder
    from .policy_object.policy_object_builder import PolicyObjectBuilder
    from .service.service_builder import ServiceBuilder
    from .sig_security.sig_security_builder import SigSecurityBuilder
    from .system.system_builder import SystemBuilder
    from .transport.transport_builder import TransportBuilder


class SdwanBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetSdwanFeatureProfileBySdwanFamilyGetResponse]:
        """
        Get all SDWAN Feature Profiles
        GET /dataservice/v1/feature-profile/sdwan

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetSdwanFeatureProfileBySdwanFamilyGetResponse]
        """
        params = {
            "offset": offset,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sdwan",
            return_type=List[GetSdwanFeatureProfileBySdwanFamilyGetResponse],
            params=params,
            **kw,
        )

    @property
    def application_priority(self) -> ApplicationPriorityBuilder:
        """
        The application-priority property
        """
        from .application_priority.application_priority_builder import ApplicationPriorityBuilder

        return ApplicationPriorityBuilder(self._request_adapter)

    @property
    def cli(self) -> CliBuilder:
        """
        The cli property
        """
        from .cli.cli_builder import CliBuilder

        return CliBuilder(self._request_adapter)

    @property
    def dns_security(self) -> DnsSecurityBuilder:
        """
        The dns-security property
        """
        from .dns_security.dns_security_builder import DnsSecurityBuilder

        return DnsSecurityBuilder(self._request_adapter)

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
    def policy_object(self) -> PolicyObjectBuilder:
        """
        The policy-object property
        """
        from .policy_object.policy_object_builder import PolicyObjectBuilder

        return PolicyObjectBuilder(self._request_adapter)

    @property
    def service(self) -> ServiceBuilder:
        """
        The service property
        """
        from .service.service_builder import ServiceBuilder

        return ServiceBuilder(self._request_adapter)

    @property
    def sig_security(self) -> SigSecurityBuilder:
        """
        The sig-security property
        """
        from .sig_security.sig_security_builder import SigSecurityBuilder

        return SigSecurityBuilder(self._request_adapter)

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
