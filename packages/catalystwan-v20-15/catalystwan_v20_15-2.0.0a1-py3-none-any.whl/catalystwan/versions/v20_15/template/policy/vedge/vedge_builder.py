# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .definition.definition_builder import DefinitionBuilder
    from .devices.devices_builder import DevicesBuilder


class VedgeBuilder:
    """
    Builds and executes requests for operations under /template/policy/vedge
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get policy details
        GET /dataservice/template/policy/vedge

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/template/policy/vedge", **kw)

    def put(self, policy_id: str, payload: Any, **kw) -> Any:
        """
        Edit template
        PUT /dataservice/template/policy/vedge/{policyId}

        :param policy_id: Policy Id
        :param payload: Template policy
        :returns: Any
        """
        params = {
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/policy/vedge/{policyId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, policy_id: str, **kw):
        """
        Delete template
        DELETE /dataservice/template/policy/vedge/{policyId}

        :param policy_id: Policy Id
        :returns: None
        """
        params = {
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/template/policy/vedge/{policyId}", params=params, **kw
        )

    @overload
    def post(self, *, policy_id: str, resource_group_name: str, **kw):
        """
        Change policy resource group
        POST /dataservice/template/policy/vedge/{resourceGroupName}/{policyId}

        :param policy_id: Policy Id
        :param resource_group_name: Resrouce group name
        :returns: None
        """
        ...

    @overload
    def post(self, *, payload: Any, **kw) -> Any:
        """
        Create template
        POST /dataservice/template/policy/vedge

        :param payload: Template policy
        :returns: Any
        """
        ...

    def post(
        self,
        *,
        payload: Optional[Any] = None,
        policy_id: Optional[str] = None,
        resource_group_name: Optional[str] = None,
        **kw,
    ) -> Union[Any, None]:
        # /dataservice/template/policy/vedge/{resourceGroupName}/{policyId}
        if self._request_adapter.param_checker(
            [(policy_id, str), (resource_group_name, str)], [payload]
        ):
            params = {
                "policyId": policy_id,
                "resourceGroupName": resource_group_name,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/template/policy/vedge/{resourceGroupName}/{policyId}",
                params=params,
                **kw,
            )
        # /dataservice/template/policy/vedge
        if self._request_adapter.param_checker([(payload, Any)], [policy_id, resource_group_name]):
            return self._request_adapter.request(
                "POST", "/dataservice/template/policy/vedge", payload=payload, **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def definition(self) -> DefinitionBuilder:
        """
        The definition property
        """
        from .definition.definition_builder import DefinitionBuilder

        return DefinitionBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)
