# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualVnfAttributesParcelPostRequest,
    CreateNfvirtualVnfAttributesParcelPostResponse,
    EditNfvirtualVnfAttributesParcelPutRequest,
    EditNfvirtualVnfAttributesParcelPutResponse,
    GetSingleNfvirtualNetworksVnfAttributesPayload,
)

if TYPE_CHECKING:
    from .vnf.vnf_builder import VnfBuilder


class VnfAttributesBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, networks_id: str, payload: CreateNfvirtualVnfAttributesParcelPostRequest, **kw
    ) -> CreateNfvirtualVnfAttributesParcelPostResponse:
        """
        Create VNF Attributes Profile config for Networks feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes

        :param networks_id: Feature Profile ID
        :param payload: VNF Attributes config Profile Parcel
        :returns: CreateNfvirtualVnfAttributesParcelPostResponse
        """
        params = {
            "networksId": networks_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes",
            return_type=CreateNfvirtualVnfAttributesParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(
        self, networks_id: str, vnf_attributes_id: str, **kw
    ) -> GetSingleNfvirtualNetworksVnfAttributesPayload:
        """
        Get VNF Attributes Profile Parcels for Networks feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}

        :param networks_id: Feature Profile ID
        :param vnf_attributes_id: Profile Parcel ID
        :returns: GetSingleNfvirtualNetworksVnfAttributesPayload
        """
        params = {
            "networksId": networks_id,
            "vnfAttributesId": vnf_attributes_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}",
            return_type=GetSingleNfvirtualNetworksVnfAttributesPayload,
            params=params,
            **kw,
        )

    def put(
        self,
        networks_id: str,
        vnf_attributes_id: str,
        payload: EditNfvirtualVnfAttributesParcelPutRequest,
        **kw,
    ) -> EditNfvirtualVnfAttributesParcelPutResponse:
        """
        Edit a VNF Attributes Profile Parcel for networks feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}

        :param networks_id: Feature Profile ID
        :param vnf_attributes_id: Profile Parcel ID
        :param payload: VNF Attributes Profile Parcel
        :returns: EditNfvirtualVnfAttributesParcelPutResponse
        """
        params = {
            "networksId": networks_id,
            "vnfAttributesId": vnf_attributes_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}",
            return_type=EditNfvirtualVnfAttributesParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, networks_id: str, vnf_attributes_id: str, **kw):
        """
        Delete VNF Attributes Profile config for Networks feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}

        :param networks_id: Feature Profile ID
        :param vnf_attributes_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "networksId": networks_id,
            "vnfAttributesId": vnf_attributes_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}",
            params=params,
            **kw,
        )

    @property
    def vnf(self) -> VnfBuilder:
        """
        The vnf property
        """
        from .vnf.vnf_builder import VnfBuilder

        return VnfBuilder(self._request_adapter)
