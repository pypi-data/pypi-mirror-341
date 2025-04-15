# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import UsersBody, UsersResponse


class UsersBuilder:
    """
    Builds and executes requests for operations under /template/policy/ise/identity/users
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: UsersBody, **kw) -> UsersResponse:
        """
        Get all identity users
        POST /dataservice/template/policy/ise/identity/users

        :param payload: Get Users from ISE associated with Active Directory Domain. Body can be empty object or null to return all users. For filtering can be like the example with a regex or a specific user.
        :returns: UsersResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/template/policy/ise/identity/users",
            return_type=UsersResponse,
            payload=payload,
            **kw,
        )
