# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .definition.definition_builder import DefinitionBuilder
    from .keyvalue.keyvalue_builder import KeyvalueBuilder


class UsergroupBuilder:
    """
    Builds and executes requests for operations under /admin/usergroup
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get all user groups
        GET /dataservice/admin/usergroup

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/admin/usergroup", return_type=List[Any], **kw
        )

    def post(self, payload: Any, **kw):
        """
        Create user group
        POST /dataservice/admin/usergroup

        :param payload: User group
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/admin/usergroup", payload=payload, **kw
        )

    def put(self, user_group_id: str, payload: Any, **kw):
        """
        Update user group
        PUT /dataservice/admin/usergroup/{userGroupId}

        :param user_group_id: User group Id
        :param payload: User group
        :returns: None
        """
        params = {
            "userGroupId": user_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/admin/usergroup/{userGroupId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, user_group_id: str, **kw):
        """
        Delete user group
        DELETE /dataservice/admin/usergroup/{userGroupId}

        :param user_group_id: User group Id
        :returns: None
        """
        params = {
            "userGroupId": user_group_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/admin/usergroup/{userGroupId}", params=params, **kw
        )

    @property
    def definition(self) -> DefinitionBuilder:
        """
        The definition property
        """
        from .definition.definition_builder import DefinitionBuilder

        return DefinitionBuilder(self._request_adapter)

    @property
    def keyvalue(self) -> KeyvalueBuilder:
        """
        The keyvalue property
        """
        from .keyvalue.keyvalue_builder import KeyvalueBuilder

        return KeyvalueBuilder(self._request_adapter)
