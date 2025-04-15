# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import UserGroupsBody, UserGroupsResponse


class UsergroupsBuilder:
    """
    Builds and executes requests for operations under /template/policy/ise/identity/usergroups
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: UserGroupsBody, **kw) -> UserGroupsResponse:
        """
        Get all identity user groups
        POST /dataservice/template/policy/ise/identity/usergroups

        :param payload: Get Users Groups from ISE associated with Active Directory Domain. Body can be an empty object or null to return all User Groups. For filtering a group must be specified, you cannot use a regex.
        :returns: UserGroupsResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/template/policy/ise/identity/usergroups",
            return_type=UserGroupsResponse,
            payload=payload,
            **kw,
        )
