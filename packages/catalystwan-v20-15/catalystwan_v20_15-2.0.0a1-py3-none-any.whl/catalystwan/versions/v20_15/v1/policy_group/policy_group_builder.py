# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreatePolicyGroupPostRequest,
    CreatePolicyGroupPostResponse,
    EditPolicyGroupPutRequest,
    EditPolicyGroupPutResponse,
    PolicyGroup,
)

if TYPE_CHECKING:
    from .device.device_builder import DeviceBuilder


class PolicyGroupBuilder:
    """
    Builds and executes requests for operations under /v1/policy-group
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: CreatePolicyGroupPostRequest, **kw) -> CreatePolicyGroupPostResponse:
        """
        Create a new Policy Group
        POST /dataservice/v1/policy-group

        :param payload: Policy Group
        :returns: CreatePolicyGroupPostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/policy-group",
            return_type=CreatePolicyGroupPostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, policy_group_id: str, payload: EditPolicyGroupPutRequest, **kw
    ) -> EditPolicyGroupPutResponse:
        """
        Edit a Policy Group
        PUT /dataservice/v1/policy-group/{policyGroupId}

        :param policy_group_id: Policy group id
        :param payload: Policy Group
        :returns: EditPolicyGroupPutResponse
        """
        params = {
            "policyGroupId": policy_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/policy-group/{policyGroupId}",
            return_type=EditPolicyGroupPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, policy_group_id: str, delete_profiles: Optional[bool] = None, **kw):
        """
        Delete Policy Group
        DELETE /dataservice/v1/policy-group/{policyGroupId}

        :param policy_group_id: Policy group id
        :param delete_profiles: Delete profiles
        :returns: None
        """
        params = {
            "policyGroupId": policy_group_id,
            "deleteProfiles": delete_profiles,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/v1/policy-group/{policyGroupId}", params=params, **kw
        )

    @overload
    def get(self, *, policy_group_id: str, **kw) -> PolicyGroup:
        """
        Get a Policy Group by ID
        GET /dataservice/v1/policy-group/{policyGroupId}

        :param policy_group_id: Policy group id
        :returns: PolicyGroup
        """
        ...

    @overload
    def get(self, *, solution: Optional[str] = None, **kw) -> List[PolicyGroup]:
        """
        Get a Policy Group by Solution
        GET /dataservice/v1/policy-group

        :param solution: Solution
        :returns: List[PolicyGroup]
        """
        ...

    def get(
        self, *, solution: Optional[str] = None, policy_group_id: Optional[str] = None, **kw
    ) -> Union[List[PolicyGroup], PolicyGroup]:
        # /dataservice/v1/policy-group/{policyGroupId}
        if self._request_adapter.param_checker([(policy_group_id, str)], [solution]):
            params = {
                "policyGroupId": policy_group_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/policy-group/{policyGroupId}",
                return_type=PolicyGroup,
                params=params,
                **kw,
            )
        # /dataservice/v1/policy-group
        if self._request_adapter.param_checker([], [policy_group_id]):
            params = {
                "solution": solution,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/policy-group",
                return_type=List[PolicyGroup],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)
