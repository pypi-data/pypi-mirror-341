# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .authcode.authcode_builder import AuthcodeBuilder
    from .get_client_id.get_client_id_builder import GetClientIdBuilder
    from .scmwidget.scmwidget_builder import ScmwidgetBuilder


class OpentaccaseBuilder:
    """
    Builds and executes requests for operations under /opentaccase
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def authcode(self) -> AuthcodeBuilder:
        """
        The authcode property
        """
        from .authcode.authcode_builder import AuthcodeBuilder

        return AuthcodeBuilder(self._request_adapter)

    @property
    def get_client_id(self) -> GetClientIdBuilder:
        """
        The getClientID property
        """
        from .get_client_id.get_client_id_builder import GetClientIdBuilder

        return GetClientIdBuilder(self._request_adapter)

    @property
    def scmwidget(self) -> ScmwidgetBuilder:
        """
        The scmwidget property
        """
        from .scmwidget.scmwidget_builder import ScmwidgetBuilder

        return ScmwidgetBuilder(self._request_adapter)
