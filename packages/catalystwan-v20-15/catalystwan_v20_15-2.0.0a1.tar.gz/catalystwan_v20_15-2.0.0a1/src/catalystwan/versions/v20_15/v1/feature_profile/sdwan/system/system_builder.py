# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanSystemFeatureProfilePostRequest,
    CreateSdwanSystemFeatureProfilePostResponse,
    EditSdwanSystemFeatureProfilePutRequest,
    EditSdwanSystemFeatureProfilePutResponse,
    GetSdwanSystemFeatureProfilesGetResponse,
    GetSingleSdwanSystemPayload,
)

if TYPE_CHECKING:
    from .aaa.aaa_builder import AaaBuilder
    from .banner.banner_builder import BannerBuilder
    from .basic.basic_builder import BasicBuilder
    from .bfd.bfd_builder import BfdBuilder
    from .global_.global_builder import GlobalBuilder
    from .logging.logging_builder import LoggingBuilder
    from .mrf.mrf_builder import MrfBuilder
    from .ntp.ntp_builder import NtpBuilder
    from .omp.omp_builder import OmpBuilder
    from .security.security_builder import SecurityBuilder
    from .snmp.snmp_builder import SnmpBuilder


class SystemBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdwanSystemFeatureProfilePostRequest, **kw
    ) -> CreateSdwanSystemFeatureProfilePostResponse:
        """
        Create a SDWAN System Feature Profile
        POST /dataservice/v1/feature-profile/sdwan/system

        :param payload: SDWAN Feature profile
        :returns: CreateSdwanSystemFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system",
            return_type=CreateSdwanSystemFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, payload: EditSdwanSystemFeatureProfilePutRequest, **kw
    ) -> EditSdwanSystemFeatureProfilePutResponse:
        """
        Edit a SDWAN System Feature Profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}

        :param system_id: Feature Profile Id
        :param payload: SDWAN Feature profile
        :returns: EditSdwanSystemFeatureProfilePutResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}",
            return_type=EditSdwanSystemFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, **kw):
        """
        Delete Feature Profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}

        :param system_id: System id
        :returns: None
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/v1/feature-profile/sdwan/system/{systemId}", params=params, **kw
        )

    @overload
    def get(self, *, system_id: str, **kw) -> GetSingleSdwanSystemPayload:
        """
        Get a SDWAN System Feature Profile with systemId
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}

        :param system_id: Feature Profile Id
        :returns: GetSingleSdwanSystemPayload
        """
        ...

    @overload
    def get(
        self, *, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetSdwanSystemFeatureProfilesGetResponse]:
        """
        Get all SDWAN Feature Profiles with giving Family and profile type
        GET /dataservice/v1/feature-profile/sdwan/system

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetSdwanSystemFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        system_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetSdwanSystemFeatureProfilesGetResponse], GetSingleSdwanSystemPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}
        if self._request_adapter.param_checker([(system_id, str)], [offset, limit]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}",
                return_type=GetSingleSdwanSystemPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system
        if self._request_adapter.param_checker([], [system_id]):
            params = {
                "offset": offset,
                "limit": limit,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system",
                return_type=List[GetSdwanSystemFeatureProfilesGetResponse],
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
    def basic(self) -> BasicBuilder:
        """
        The basic property
        """
        from .basic.basic_builder import BasicBuilder

        return BasicBuilder(self._request_adapter)

    @property
    def bfd(self) -> BfdBuilder:
        """
        The bfd property
        """
        from .bfd.bfd_builder import BfdBuilder

        return BfdBuilder(self._request_adapter)

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
    def mrf(self) -> MrfBuilder:
        """
        The mrf property
        """
        from .mrf.mrf_builder import MrfBuilder

        return MrfBuilder(self._request_adapter)

    @property
    def ntp(self) -> NtpBuilder:
        """
        The ntp property
        """
        from .ntp.ntp_builder import NtpBuilder

        return NtpBuilder(self._request_adapter)

    @property
    def omp(self) -> OmpBuilder:
        """
        The omp property
        """
        from .omp.omp_builder import OmpBuilder

        return OmpBuilder(self._request_adapter)

    @property
    def security(self) -> SecurityBuilder:
        """
        The security property
        """
        from .security.security_builder import SecurityBuilder

        return SecurityBuilder(self._request_adapter)

    @property
    def snmp(self) -> SnmpBuilder:
        """
        The snmp property
        """
        from .snmp.snmp_builder import SnmpBuilder

        return SnmpBuilder(self._request_adapter)
