# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .setting.setting_builder import SettingBuilder


class UpgradeBuilder:
    """
    Builds and executes requests for operations under /device/action/ztp/upgrade
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get ZTP upgrade configuration
        GET /dataservice/device/action/ztp/upgrade

        :returns: None
        """
        return self._request_adapter.request("GET", "/dataservice/device/action/ztp/upgrade", **kw)

    def post(self, payload: Any, **kw):
        """
        Process ZTP upgrade configuration setting
        POST /dataservice/device/action/ztp/upgrade

        :param payload: Request body for ZTP upgrade configuration setting
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/ztp/upgrade", payload=payload, **kw
        )

    @property
    def setting(self) -> SettingBuilder:
        """
        The setting property
        """
        from .setting.setting_builder import SettingBuilder

        return SettingBuilder(self._request_adapter)
