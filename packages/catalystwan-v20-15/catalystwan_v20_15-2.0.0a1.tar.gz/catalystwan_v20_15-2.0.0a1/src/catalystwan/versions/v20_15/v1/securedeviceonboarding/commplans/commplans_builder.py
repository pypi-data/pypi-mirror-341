# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CommunicationPlansResponse


class CommplansBuilder:
    """
    Builds and executes requests for operations under /v1/securedeviceonboarding/{accountId}/commplans
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, account_id: str, **kw) -> CommunicationPlansResponse:
        """
        Get communication plans by account Id
        GET /dataservice/v1/securedeviceonboarding/{accountId}/commplans

        :param account_id: Service User Account ID
        :returns: CommunicationPlansResponse
        """
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/securedeviceonboarding/{accountId}/commplans",
            return_type=CommunicationPlansResponse,
            params=params,
            **kw,
        )
