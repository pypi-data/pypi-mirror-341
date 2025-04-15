# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import MapDevicesRequest, PartnerDevicesRes, StatusResponse


class MapBuilder:
    """
    Builds and executes requests for operations under /partner/{partnerType}/map
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, partner_type: str, nms_id: str, **kw) -> PartnerDevicesRes:
        """
        List mapped devices for the partner
        GET /dataservice/partner/{partnerType}/map/{nmsId}

        :param partner_type: Partner type
        :param nms_id: Nms id
        :returns: PartnerDevicesRes
        """
        params = {
            "partnerType": partner_type,
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/partner/{partnerType}/map/{nmsId}",
            return_type=PartnerDevicesRes,
            params=params,
            **kw,
        )

    def post(
        self, partner_type: str, nms_id: str, payload: MapDevicesRequest, **kw
    ) -> StatusResponse:
        """
        Map devices for the partner
        POST /dataservice/partner/{partnerType}/map/{nmsId}

        :param partner_type: Partner type
        :param nms_id: Nms id
        :param payload: List of devices
        :returns: StatusResponse
        """
        params = {
            "partnerType": partner_type,
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/partner/{partnerType}/map/{nmsId}",
            return_type=StatusResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, partner_type: str, nms_id: str, **kw) -> StatusResponse:
        """
        Unmap all devices for the partner
        DELETE /dataservice/partner/{partnerType}/map/{nmsId}

        :param partner_type: Partner type
        :param nms_id: Nms id
        :returns: StatusResponse
        """
        params = {
            "partnerType": partner_type,
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/partner/{partnerType}/map/{nmsId}",
            return_type=StatusResponse,
            params=params,
            **kw,
        )
