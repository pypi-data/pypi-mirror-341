# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest1,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest2,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest3,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest4,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest5,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest6,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest7,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest8,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest9,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest10,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest11,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest12,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest13,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest14,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest15,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest16,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest17,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest18,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest19,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest20,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest21,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest22,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest23,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest24,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest25,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest26,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest27,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest28,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest29,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest30,
    CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest1,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest2,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest3,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest4,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest5,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest6,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest7,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest8,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest9,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest10,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest11,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest12,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest13,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest14,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest15,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest16,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest17,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest18,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest19,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest20,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest21,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest22,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest23,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest24,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest25,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest26,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest27,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest28,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest29,
    EditDataPrefixProfileParcelForPolicyObjectPutRequest30,
    EditDataPrefixProfileParcelForPolicyObjectPutResponse,
    GetListSdwanPolicyObjectSecurityDataIpPrefixPayload,
    GetSingleSdwanPolicyObjectSecurityDataIpPrefixPayload,
    PolicyObjectListTypeParam,
)

if TYPE_CHECKING:
    from .app_list.app_list_builder import AppListBuilder
    from .app_probe.app_probe_builder import AppProbeBuilder
    from .as_path.as_path_builder import AsPathBuilder
    from .class_.class_builder import ClassBuilder
    from .color.color_builder import ColorBuilder
    from .data_ipv6_prefix.data_ipv6_prefix_builder import DataIpv6PrefixBuilder
    from .data_prefix.data_prefix_builder import DataPrefixBuilder
    from .expanded_community.expanded_community_builder import ExpandedCommunityBuilder
    from .ext_community.ext_community_builder import ExtCommunityBuilder
    from .ipv6_prefix.ipv6_prefix_builder import Ipv6PrefixBuilder
    from .mirror.mirror_builder import MirrorBuilder
    from .policer.policer_builder import PolicerBuilder
    from .preferred_color_group.preferred_color_group_builder import PreferredColorGroupBuilder
    from .prefix.prefix_builder import PrefixBuilder
    from .schema.schema_builder import SchemaBuilder
    from .security_data_ip_prefix.security_data_ip_prefix_builder import SecurityDataIpPrefixBuilder
    from .security_fqdn.security_fqdn_builder import SecurityFqdnBuilder
    from .security_geolocation.security_geolocation_builder import SecurityGeolocationBuilder
    from .security_identity.security_identity_builder import SecurityIdentityBuilder
    from .security_ipssignature.security_ipssignature_builder import SecurityIpssignatureBuilder
    from .security_localapp.security_localapp_builder import SecurityLocalappBuilder
    from .security_localdomain.security_localdomain_builder import SecurityLocaldomainBuilder
    from .security_port.security_port_builder import SecurityPortBuilder
    from .security_protocolname.security_protocolname_builder import SecurityProtocolnameBuilder
    from .security_scalablegrouptag.security_scalablegrouptag_builder import (
        SecurityScalablegrouptagBuilder,
    )
    from .security_urllist.security_urllist_builder import SecurityUrllistBuilder
    from .security_zone.security_zone_builder import SecurityZoneBuilder
    from .sla_class.sla_class_builder import SlaClassBuilder
    from .standard_community.standard_community_builder import StandardCommunityBuilder
    from .tloc.tloc_builder import TlocBuilder
    from .unified.unified_builder import UnifiedBuilder
    from .vpn_group.vpn_group_builder import VpnGroupBuilder


class PolicyObjectBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/policy-object
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        policy_object_id: str,
        policy_object_list_type: PolicyObjectListTypeParam,
        payload: Union[
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest1,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest2,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest3,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest4,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest5,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest6,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest7,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest8,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest9,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest10,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest11,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest12,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest13,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest14,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest15,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest16,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest17,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest18,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest19,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest20,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest21,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest22,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest23,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest24,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest25,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest26,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest27,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest28,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest29,
            CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest30,
        ],
        **kw,
    ) -> CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse:
        """
        Create a Data Prefix Profile Parcel for Security Policy Object feature profile
        POST /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}

        :param policy_object_id: Feature Profile ID
        :param policy_object_list_type: Policy Object ListType
        :param payload: Data Prefix Profile Parcel
        :returns: CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse
        """
        params = {
            "policyObjectId": policy_object_id,
            "policyObjectListType": policy_object_list_type,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}",
            return_type=CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        policy_object_id: str,
        policy_object_list_type: PolicyObjectListTypeParam,
        list_object_id: str,
        payload: Union[
            EditDataPrefixProfileParcelForPolicyObjectPutRequest1,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest2,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest3,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest4,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest5,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest6,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest7,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest8,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest9,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest10,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest11,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest12,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest13,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest14,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest15,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest16,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest17,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest18,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest19,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest20,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest21,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest22,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest23,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest24,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest25,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest26,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest27,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest28,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest29,
            EditDataPrefixProfileParcelForPolicyObjectPutRequest30,
        ],
        **kw,
    ) -> EditDataPrefixProfileParcelForPolicyObjectPutResponse:
        """
        Update a Data Prefix Profile Parcel for Policy Object feature profile
        PUT /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}/{listObjectId}

        :param policy_object_id: Feature Profile ID
        :param policy_object_list_type: Policy Object ListType
        :param list_object_id: Profile Parcel ID
        :param payload: Data Prefix Profile Parcel
        :returns: EditDataPrefixProfileParcelForPolicyObjectPutResponse
        """
        params = {
            "policyObjectId": policy_object_id,
            "policyObjectListType": policy_object_list_type,
            "listObjectId": list_object_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}/{listObjectId}",
            return_type=EditDataPrefixProfileParcelForPolicyObjectPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self,
        policy_object_id: str,
        policy_object_list_type: PolicyObjectListTypeParam,
        list_object_id: str,
        **kw,
    ):
        """
        Delete a Data Prefix Profile Parcel for Policy Object feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}/{listObjectId}

        :param policy_object_id: Feature Profile ID
        :param policy_object_list_type: Policy Object ListType
        :param list_object_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "policyObjectId": policy_object_id,
            "policyObjectListType": policy_object_list_type,
            "listObjectId": list_object_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}/{listObjectId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self,
        *,
        policy_object_id: str,
        policy_object_list_type: PolicyObjectListTypeParam,
        list_object_id: str,
        references: Optional[bool] = False,
        **kw,
    ) -> GetSingleSdwanPolicyObjectSecurityDataIpPrefixPayload:
        """
        Get Data Prefix Profile Parcel by parcelId for Policy Object feature profile
        GET /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}/{listObjectId}

        :param policy_object_id: Feature Profile ID
        :param policy_object_list_type: Policy Object ListType
        :param list_object_id: Profile Parcel ID
        :param references: get referred profile/parcel details
        :returns: GetSingleSdwanPolicyObjectSecurityDataIpPrefixPayload
        """
        ...

    @overload
    def get(
        self,
        *,
        policy_object_id: str,
        policy_object_list_type: PolicyObjectListTypeParam,
        reference_count: Optional[bool] = False,
        **kw,
    ) -> GetListSdwanPolicyObjectSecurityDataIpPrefixPayload:
        """
        Get Data Prefix Profile Parcels for Policy Object feature profile
        GET /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}

        :param policy_object_id: Feature Profile ID
        :param policy_object_list_type: Policy Object ListType
        :param reference_count: get reference count
        :returns: GetListSdwanPolicyObjectSecurityDataIpPrefixPayload
        """
        ...

    def get(
        self,
        *,
        policy_object_id: str,
        policy_object_list_type: PolicyObjectListTypeParam,
        reference_count: Optional[bool] = None,
        list_object_id: Optional[str] = None,
        references: Optional[bool] = None,
        **kw,
    ) -> Union[
        GetListSdwanPolicyObjectSecurityDataIpPrefixPayload,
        GetSingleSdwanPolicyObjectSecurityDataIpPrefixPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}/{listObjectId}
        if self._request_adapter.param_checker(
            [
                (policy_object_id, str),
                (policy_object_list_type, PolicyObjectListTypeParam),
                (list_object_id, str),
            ],
            [reference_count],
        ):
            params = {
                "policyObjectId": policy_object_id,
                "policyObjectListType": policy_object_list_type,
                "listObjectId": list_object_id,
                "references": references,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}/{listObjectId}",
                return_type=GetSingleSdwanPolicyObjectSecurityDataIpPrefixPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}
        if self._request_adapter.param_checker(
            [(policy_object_id, str), (policy_object_list_type, PolicyObjectListTypeParam)],
            [list_object_id, references],
        ):
            params = {
                "policyObjectId": policy_object_id,
                "policyObjectListType": policy_object_list_type,
                "referenceCount": reference_count,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/{policyObjectListType}",
                return_type=GetListSdwanPolicyObjectSecurityDataIpPrefixPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def app_list(self) -> AppListBuilder:
        """
        The app-list property
        """
        from .app_list.app_list_builder import AppListBuilder

        return AppListBuilder(self._request_adapter)

    @property
    def app_probe(self) -> AppProbeBuilder:
        """
        The app-probe property
        """
        from .app_probe.app_probe_builder import AppProbeBuilder

        return AppProbeBuilder(self._request_adapter)

    @property
    def as_path(self) -> AsPathBuilder:
        """
        The as-path property
        """
        from .as_path.as_path_builder import AsPathBuilder

        return AsPathBuilder(self._request_adapter)

    @property
    def class_(self) -> ClassBuilder:
        """
        The class property
        """
        from .class_.class_builder import ClassBuilder

        return ClassBuilder(self._request_adapter)

    @property
    def color(self) -> ColorBuilder:
        """
        The color property
        """
        from .color.color_builder import ColorBuilder

        return ColorBuilder(self._request_adapter)

    @property
    def data_ipv6_prefix(self) -> DataIpv6PrefixBuilder:
        """
        The data-ipv6-prefix property
        """
        from .data_ipv6_prefix.data_ipv6_prefix_builder import DataIpv6PrefixBuilder

        return DataIpv6PrefixBuilder(self._request_adapter)

    @property
    def data_prefix(self) -> DataPrefixBuilder:
        """
        The data-prefix property
        """
        from .data_prefix.data_prefix_builder import DataPrefixBuilder

        return DataPrefixBuilder(self._request_adapter)

    @property
    def expanded_community(self) -> ExpandedCommunityBuilder:
        """
        The expanded-community property
        """
        from .expanded_community.expanded_community_builder import ExpandedCommunityBuilder

        return ExpandedCommunityBuilder(self._request_adapter)

    @property
    def ext_community(self) -> ExtCommunityBuilder:
        """
        The ext-community property
        """
        from .ext_community.ext_community_builder import ExtCommunityBuilder

        return ExtCommunityBuilder(self._request_adapter)

    @property
    def ipv6_prefix(self) -> Ipv6PrefixBuilder:
        """
        The ipv6-prefix property
        """
        from .ipv6_prefix.ipv6_prefix_builder import Ipv6PrefixBuilder

        return Ipv6PrefixBuilder(self._request_adapter)

    @property
    def mirror(self) -> MirrorBuilder:
        """
        The mirror property
        """
        from .mirror.mirror_builder import MirrorBuilder

        return MirrorBuilder(self._request_adapter)

    @property
    def policer(self) -> PolicerBuilder:
        """
        The policer property
        """
        from .policer.policer_builder import PolicerBuilder

        return PolicerBuilder(self._request_adapter)

    @property
    def preferred_color_group(self) -> PreferredColorGroupBuilder:
        """
        The preferred-color-group property
        """
        from .preferred_color_group.preferred_color_group_builder import PreferredColorGroupBuilder

        return PreferredColorGroupBuilder(self._request_adapter)

    @property
    def prefix(self) -> PrefixBuilder:
        """
        The prefix property
        """
        from .prefix.prefix_builder import PrefixBuilder

        return PrefixBuilder(self._request_adapter)

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)

    @property
    def security_data_ip_prefix(self) -> SecurityDataIpPrefixBuilder:
        """
        The security-data-ip-prefix property
        """
        from .security_data_ip_prefix.security_data_ip_prefix_builder import (
            SecurityDataIpPrefixBuilder,
        )

        return SecurityDataIpPrefixBuilder(self._request_adapter)

    @property
    def security_fqdn(self) -> SecurityFqdnBuilder:
        """
        The security-fqdn property
        """
        from .security_fqdn.security_fqdn_builder import SecurityFqdnBuilder

        return SecurityFqdnBuilder(self._request_adapter)

    @property
    def security_geolocation(self) -> SecurityGeolocationBuilder:
        """
        The security-geolocation property
        """
        from .security_geolocation.security_geolocation_builder import SecurityGeolocationBuilder

        return SecurityGeolocationBuilder(self._request_adapter)

    @property
    def security_identity(self) -> SecurityIdentityBuilder:
        """
        The security-identity property
        """
        from .security_identity.security_identity_builder import SecurityIdentityBuilder

        return SecurityIdentityBuilder(self._request_adapter)

    @property
    def security_ipssignature(self) -> SecurityIpssignatureBuilder:
        """
        The security-ipssignature property
        """
        from .security_ipssignature.security_ipssignature_builder import SecurityIpssignatureBuilder

        return SecurityIpssignatureBuilder(self._request_adapter)

    @property
    def security_localapp(self) -> SecurityLocalappBuilder:
        """
        The security-localapp property
        """
        from .security_localapp.security_localapp_builder import SecurityLocalappBuilder

        return SecurityLocalappBuilder(self._request_adapter)

    @property
    def security_localdomain(self) -> SecurityLocaldomainBuilder:
        """
        The security-localdomain property
        """
        from .security_localdomain.security_localdomain_builder import SecurityLocaldomainBuilder

        return SecurityLocaldomainBuilder(self._request_adapter)

    @property
    def security_port(self) -> SecurityPortBuilder:
        """
        The security-port property
        """
        from .security_port.security_port_builder import SecurityPortBuilder

        return SecurityPortBuilder(self._request_adapter)

    @property
    def security_protocolname(self) -> SecurityProtocolnameBuilder:
        """
        The security-protocolname property
        """
        from .security_protocolname.security_protocolname_builder import SecurityProtocolnameBuilder

        return SecurityProtocolnameBuilder(self._request_adapter)

    @property
    def security_scalablegrouptag(self) -> SecurityScalablegrouptagBuilder:
        """
        The security-scalablegrouptag property
        """
        from .security_scalablegrouptag.security_scalablegrouptag_builder import (
            SecurityScalablegrouptagBuilder,
        )

        return SecurityScalablegrouptagBuilder(self._request_adapter)

    @property
    def security_urllist(self) -> SecurityUrllistBuilder:
        """
        The security-urllist property
        """
        from .security_urllist.security_urllist_builder import SecurityUrllistBuilder

        return SecurityUrllistBuilder(self._request_adapter)

    @property
    def security_zone(self) -> SecurityZoneBuilder:
        """
        The security-zone property
        """
        from .security_zone.security_zone_builder import SecurityZoneBuilder

        return SecurityZoneBuilder(self._request_adapter)

    @property
    def sla_class(self) -> SlaClassBuilder:
        """
        The sla-class property
        """
        from .sla_class.sla_class_builder import SlaClassBuilder

        return SlaClassBuilder(self._request_adapter)

    @property
    def standard_community(self) -> StandardCommunityBuilder:
        """
        The standard-community property
        """
        from .standard_community.standard_community_builder import StandardCommunityBuilder

        return StandardCommunityBuilder(self._request_adapter)

    @property
    def tloc(self) -> TlocBuilder:
        """
        The tloc property
        """
        from .tloc.tloc_builder import TlocBuilder

        return TlocBuilder(self._request_adapter)

    @property
    def unified(self) -> UnifiedBuilder:
        """
        The unified property
        """
        from .unified.unified_builder import UnifiedBuilder

        return UnifiedBuilder(self._request_adapter)

    @property
    def vpn_group(self) -> VpnGroupBuilder:
        """
        The vpn-group property
        """
        from .vpn_group.vpn_group_builder import VpnGroupBuilder

        return VpnGroupBuilder(self._request_adapter)
