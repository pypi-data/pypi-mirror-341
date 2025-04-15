# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cloudconnector.cloudconnector_builder import CloudconnectorBuilder
    from .customapps.customapps_builder import CustomappsBuilder
    from .protocol_pack.protocol_pack_builder import ProtocolPackBuilder
    from .task.task_builder import TaskBuilder
    from .test.test_builder import TestBuilder


class SdavcBuilder:
    """
    Builds and executes requests for operations under /sdavc
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cloudconnector(self) -> CloudconnectorBuilder:
        """
        The cloudconnector property
        """
        from .cloudconnector.cloudconnector_builder import CloudconnectorBuilder

        return CloudconnectorBuilder(self._request_adapter)

    @property
    def customapps(self) -> CustomappsBuilder:
        """
        The customapps property
        """
        from .customapps.customapps_builder import CustomappsBuilder

        return CustomappsBuilder(self._request_adapter)

    @property
    def protocol_pack(self) -> ProtocolPackBuilder:
        """
        The protocol-pack property
        """
        from .protocol_pack.protocol_pack_builder import ProtocolPackBuilder

        return ProtocolPackBuilder(self._request_adapter)

    @property
    def task(self) -> TaskBuilder:
        """
        The task property
        """
        from .task.task_builder import TaskBuilder

        return TaskBuilder(self._request_adapter)

    @property
    def test(self) -> TestBuilder:
        """
        The test property
        """
        from .test.test_builder import TestBuilder

        return TestBuilder(self._request_adapter)
