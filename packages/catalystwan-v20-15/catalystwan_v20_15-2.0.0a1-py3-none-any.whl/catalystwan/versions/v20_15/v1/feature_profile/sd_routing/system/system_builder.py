# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingSystemFeatureProfilePostRequest,
    CreateSdroutingSystemFeatureProfilePostResponse,
    EditSdroutingSystemFeatureProfilePutRequest,
    EditSdroutingSystemFeatureProfilePutResponse,
    GetSdroutingSystemFeatureProfilesGetResponse,
    GetSingleSdRoutingSystemPayload,
)

if TYPE_CHECKING:
    from .aaa.aaa_builder import AaaBuilder
    from .banner.banner_builder import BannerBuilder
    from .certificate.certificate_builder import CertificateBuilder
    from .flexible_port_speed.flexible_port_speed_builder import FlexiblePortSpeedBuilder
    from .global_.global_builder import GlobalBuilder
    from .logging.logging_builder import LoggingBuilder
    from .ntp.ntp_builder import NtpBuilder
    from .snmp.snmp_builder import SnmpBuilder


class SystemBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/system
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdroutingSystemFeatureProfilePostRequest, **kw
    ) -> CreateSdroutingSystemFeatureProfilePostResponse:
        """
        Create a SD-Routing System Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/system

        :param payload: SD-Routing System Feature Profile
        :returns: CreateSdroutingSystemFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/system",
            return_type=CreateSdroutingSystemFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, payload: EditSdroutingSystemFeatureProfilePutRequest, **kw
    ) -> EditSdroutingSystemFeatureProfilePutResponse:
        """
        Edit a SD-Routing System Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/system/{systemId}

        :param system_id: System Profile Id
        :param payload: SD-Routing System Feature Profile
        :returns: EditSdroutingSystemFeatureProfilePutResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}",
            return_type=EditSdroutingSystemFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, **kw):
        """
        Delete a SD-Routing System Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/system/{systemId}

        :param system_id: System Profile Id
        :returns: None
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, *, system_id: str, **kw) -> GetSingleSdRoutingSystemPayload:
        """
        Get a SD-Routing System Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}

        :param system_id: System Profile Id
        :returns: GetSingleSdRoutingSystemPayload
        """
        ...

    @overload
    def get(
        self, *, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetSdroutingSystemFeatureProfilesGetResponse]:
        """
        Get all SD-Routing System Feature Profiles
        GET /dataservice/v1/feature-profile/sd-routing/system

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetSdroutingSystemFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        system_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetSdroutingSystemFeatureProfilesGetResponse], GetSingleSdRoutingSystemPayload]:
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}
        if self._request_adapter.param_checker([(system_id, str)], [offset, limit]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}",
                return_type=GetSingleSdRoutingSystemPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/system
        if self._request_adapter.param_checker([], [system_id]):
            params = {
                "offset": offset,
                "limit": limit,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system",
                return_type=List[GetSdroutingSystemFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def aaa(self) -> AaaBuilder:
        """
        The aaa property
        """
        from .aaa.aaa_builder import AaaBuilder

        return AaaBuilder(self._request_adapter)

    @property
    def banner(self) -> BannerBuilder:
        """
        The banner property
        """
        from .banner.banner_builder import BannerBuilder

        return BannerBuilder(self._request_adapter)

    @property
    def certificate(self) -> CertificateBuilder:
        """
        The certificate property
        """
        from .certificate.certificate_builder import CertificateBuilder

        return CertificateBuilder(self._request_adapter)

    @property
    def flexible_port_speed(self) -> FlexiblePortSpeedBuilder:
        """
        The flexible-port-speed property
        """
        from .flexible_port_speed.flexible_port_speed_builder import FlexiblePortSpeedBuilder

        return FlexiblePortSpeedBuilder(self._request_adapter)

    @property
    def global_(self) -> GlobalBuilder:
        """
        The global property
        """
        from .global_.global_builder import GlobalBuilder

        return GlobalBuilder(self._request_adapter)

    @property
    def logging(self) -> LoggingBuilder:
        """
        The logging property
        """
        from .logging.logging_builder import LoggingBuilder

        return LoggingBuilder(self._request_adapter)

    @property
    def ntp(self) -> NtpBuilder:
        """
        The ntp property
        """
        from .ntp.ntp_builder import NtpBuilder

        return NtpBuilder(self._request_adapter)

    @property
    def snmp(self) -> SnmpBuilder:
        """
        The snmp property
        """
        from .snmp.snmp_builder import SnmpBuilder

        return SnmpBuilder(self._request_adapter)
