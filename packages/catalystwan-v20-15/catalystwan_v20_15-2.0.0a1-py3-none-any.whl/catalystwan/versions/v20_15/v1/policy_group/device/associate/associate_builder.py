# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreatePolicyGroupAssociationPostRequest,
    DeletePolicyGroupAssociationDeleteRequest,
    UpdatePolicyGroupAssociationPutRequest,
)


class AssociateBuilder:
    """
    Builds and executes requests for operations under /v1/policy-group/{policyGroupId}/device/associate
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, policy_group_id: str, **kw):
        """
        Get devices association with a policy group
        GET /dataservice/v1/policy-group/{policyGroupId}/device/associate

        :param policy_group_id: Policy group id
        :returns: None
        """
        params = {
            "policyGroupId": policy_group_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/policy-group/{policyGroupId}/device/associate",
            params=params,
            **kw,
        )

    def put(self, policy_group_id: str, payload: UpdatePolicyGroupAssociationPutRequest, **kw):
        """
        Move the devices from one policy group to another
        PUT /dataservice/v1/policy-group/{policyGroupId}/device/associate

        :param policy_group_id: Policy group id
        :param payload: Payload
        :returns: None
        """
        params = {
            "policyGroupId": policy_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/policy-group/{policyGroupId}/device/associate",
            params=params,
            payload=payload,
            **kw,
        )

    def post(self, policy_group_id: str, payload: CreatePolicyGroupAssociationPostRequest, **kw):
        """
        Create associations with device and a policy group
        POST /dataservice/v1/policy-group/{policyGroupId}/device/associate

        :param policy_group_id: Policy group id
        :param payload: Payload
        :returns: None
        """
        params = {
            "policyGroupId": policy_group_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/policy-group/{policyGroupId}/device/associate",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self,
        policy_group_id: str,
        payload: Optional[DeletePolicyGroupAssociationDeleteRequest] = None,
        **kw,
    ):
        """
        Delete Policy Group Association from devices
        DELETE /dataservice/v1/policy-group/{policyGroupId}/device/associate

        :param policy_group_id: Policy group id
        :param payload: Payload
        :returns: None
        """
        params = {
            "policyGroupId": policy_group_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/policy-group/{policyGroupId}/device/associate",
            params=params,
            payload=payload,
            **kw,
        )
