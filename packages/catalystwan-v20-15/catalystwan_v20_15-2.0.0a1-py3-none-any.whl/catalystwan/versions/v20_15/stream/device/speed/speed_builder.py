# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    SpeedTestResponse,
    SpeedTestResult,
    SpeedTestResultResponse,
    SpeedTestSession,
    SpeedTestStatusResponse,
    Uuid,
)

if TYPE_CHECKING:
    from .disable.disable_builder import DisableBuilder
    from .interface.interface_builder import InterfaceBuilder
    from .start.start_builder import StartBuilder
    from .status.status_builder import StatusBuilder
    from .stop.stop_builder import StopBuilder


class SpeedBuilder:
    """
    Builds and executes requests for operations under /stream/device/speed
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, session_id: Uuid, log_id: Optional[int] = 0, **kw) -> SpeedTestResultResponse:
        """
        Get
        GET /dataservice/stream/device/speed/{sessionId}

        :param session_id: sessionId
        :param log_id: Log id
        :returns: SpeedTestResultResponse
        """
        params = {
            "sessionId": session_id,
            "logId": log_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/speed/{sessionId}",
            return_type=SpeedTestResultResponse,
            params=params,
            **kw,
        )

    @overload
    def post(
        self, payload: SpeedTestResult, device_uuid: str, session_id: Uuid, **kw
    ) -> SpeedTestStatusResponse:
        """
        Save speed test results
        POST /dataservice/stream/device/speed/{deviceUUID}/{sessionId}

        :param payload: SpeedTestResult
        :param device_uuid: Device uuid
        :param session_id: sessionId
        :returns: SpeedTestStatusResponse
        """
        ...

    @overload
    def post(self, payload: SpeedTestSession, **kw) -> SpeedTestResponse:
        """
        Get session
        POST /dataservice/stream/device/speed

        :param payload: Payload
        :returns: SpeedTestResponse
        """
        ...

    def post(
        self,
        payload: Union[SpeedTestSession, SpeedTestResult],
        device_uuid: Optional[str] = None,
        session_id: Optional[Uuid] = None,
        **kw,
    ) -> Union[SpeedTestResponse, SpeedTestStatusResponse]:
        # /dataservice/stream/device/speed/{deviceUUID}/{sessionId}
        if self._request_adapter.param_checker(
            [(payload, SpeedTestResult), (device_uuid, str), (session_id, Uuid)], []
        ):
            params = {
                "deviceUUID": device_uuid,
                "sessionId": session_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/stream/device/speed/{deviceUUID}/{sessionId}",
                return_type=SpeedTestStatusResponse,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/stream/device/speed
        if self._request_adapter.param_checker(
            [(payload, SpeedTestSession)], [device_uuid, session_id]
        ):
            return self._request_adapter.request(
                "POST",
                "/dataservice/stream/device/speed",
                return_type=SpeedTestResponse,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def disable(self) -> DisableBuilder:
        """
        The disable property
        """
        from .disable.disable_builder import DisableBuilder

        return DisableBuilder(self._request_adapter)

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def start(self) -> StartBuilder:
        """
        The start property
        """
        from .start.start_builder import StartBuilder

        return StartBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def stop(self) -> StopBuilder:
        """
        The stop property
        """
        from .stop.stop_builder import StopBuilder

        return StopBuilder(self._request_adapter)
