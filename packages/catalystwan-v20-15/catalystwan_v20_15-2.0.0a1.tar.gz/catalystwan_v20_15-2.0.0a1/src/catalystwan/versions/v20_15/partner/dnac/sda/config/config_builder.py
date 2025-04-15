# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SdaConfigRequest, SdaDeviceConfigRes


class ConfigBuilder:
    """
    Builds and executes requests for operations under /partner/dnac/sda/config
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, partner_id: str, payload: SdaConfigRequest, **kw) -> SdaDeviceConfigRes:
        """
        Create SDA enabled device
        POST /dataservice/partner/dnac/sda/config/{partnerId}

        :param partner_id: Partner id
        :param payload: Device SDA configuration
        :returns: SdaDeviceConfigRes
        """
        params = {
            "partnerId": partner_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/partner/dnac/sda/config/{partnerId}",
            return_type=SdaDeviceConfigRes,
            params=params,
            payload=payload,
            **kw,
        )
