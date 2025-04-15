# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import MapDevicesRequest, StatusResponse


class UnmapBuilder:
    """
    Builds and executes requests for operations under /partner/{partnerType}/unmap
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, partner_type: str, nms_id: str, payload: MapDevicesRequest, **kw
    ) -> StatusResponse:
        """
        Unmap a set of devices for the partner
        POST /dataservice/partner/{partnerType}/unmap/{nmsId}

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
            "/dataservice/partner/{partnerType}/unmap/{nmsId}",
            return_type=StatusResponse,
            params=params,
            payload=payload,
            **kw,
        )
