# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import FirmwareImageRemoteUpgrade

if TYPE_CHECKING:
    from .devices.devices_builder import DevicesBuilder
    from .remote.remote_builder import RemoteBuilder


class FirmwareUpgradeBuilder:
    """
    Builds and executes requests for operations under /device/action/firmware-upgrade
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> FirmwareImageRemoteUpgrade:
        """
        Eemote firmware on device
        POST /dataservice/device/action/firmware-upgrade

        :param payload: Request body
        :returns: FirmwareImageRemoteUpgrade
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/action/firmware-upgrade",
            return_type=FirmwareImageRemoteUpgrade,
            payload=payload,
            **kw,
        )

    def delete(self, version_id: str, **kw):
        """
        Download software package file
        DELETE /dataservice/device/action/firmware-upgrade/{versionId}

        :param version_id: Version id
        :returns: None
        """
        params = {
            "versionId": version_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/device/action/firmware-upgrade/{versionId}", params=params, **kw
        )

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)

    @property
    def remote(self) -> RemoteBuilder:
        """
        The remote property
        """
        from .remote.remote_builder import RemoteBuilder

        return RemoteBuilder(self._request_adapter)
