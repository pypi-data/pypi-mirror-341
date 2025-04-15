# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .attachment.attachment_builder import AttachmentBuilder
    from .circuit.circuit_builder import CircuitBuilder
    from .global_.global_builder import GlobalBuilder
    from .lock.lock_builder import LockBuilder
    from .mytest.mytest_builder import MytestBuilder
    from .profile.profile_builder import ProfileBuilder
    from .service_profile_config.service_profile_config_builder import ServiceProfileConfigBuilder


class NetworkdesignBuilder:
    """
    Builds and executes requests for operations under /networkdesign
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get existing network design
        GET /dataservice/networkdesign

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getNetworkDesign")
        return self._request_adapter.request("GET", "/dataservice/networkdesign", **kw)

    def put(self, id: str, payload: Any, **kw) -> Any:
        """
        Edit network segment
        PUT /dataservice/networkdesign

        :param id: Id
        :param payload: Network design payload
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "editNetworkDesign")
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/networkdesign", params=params, payload=payload, **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Create network design
        POST /dataservice/networkdesign

        :param payload: Network design payload
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "createNetworkDesign")
        return self._request_adapter.request(
            "POST", "/dataservice/networkdesign", payload=payload, **kw
        )

    @property
    def attachment(self) -> AttachmentBuilder:
        """
        The attachment property
        """
        from .attachment.attachment_builder import AttachmentBuilder

        return AttachmentBuilder(self._request_adapter)

    @property
    def circuit(self) -> CircuitBuilder:
        """
        The circuit property
        """
        from .circuit.circuit_builder import CircuitBuilder

        return CircuitBuilder(self._request_adapter)

    @property
    def global_(self) -> GlobalBuilder:
        """
        The global property
        """
        from .global_.global_builder import GlobalBuilder

        return GlobalBuilder(self._request_adapter)

    @property
    def lock(self) -> LockBuilder:
        """
        The lock property
        """
        from .lock.lock_builder import LockBuilder

        return LockBuilder(self._request_adapter)

    @property
    def mytest(self) -> MytestBuilder:
        """
        The mytest property
        """
        from .mytest.mytest_builder import MytestBuilder

        return MytestBuilder(self._request_adapter)

    @property
    def profile(self) -> ProfileBuilder:
        """
        The profile property
        """
        from .profile.profile_builder import ProfileBuilder

        return ProfileBuilder(self._request_adapter)

    @property
    def service_profile_config(self) -> ServiceProfileConfigBuilder:
        """
        The serviceProfileConfig property
        """
        from .service_profile_config.service_profile_config_builder import (
            ServiceProfileConfigBuilder,
        )

        return ServiceProfileConfigBuilder(self._request_adapter)
