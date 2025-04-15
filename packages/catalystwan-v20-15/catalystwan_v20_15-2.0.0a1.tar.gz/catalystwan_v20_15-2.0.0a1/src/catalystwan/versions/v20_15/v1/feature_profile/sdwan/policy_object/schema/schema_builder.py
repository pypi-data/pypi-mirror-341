# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PolicyObjectListTypeParam, SchemaTypeParam


class SchemaBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/policy-object/{policyObjectListType}/schema
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, schema_type: SchemaTypeParam, policy_object_list_type: PolicyObjectListTypeParam, **kw
    ) -> str:
        """
        Get a SDWAN PolicyObject DataPrefix Parcel Schema by Schema Type
        GET /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectListType}/schema

        :param schema_type: Schema type
        :param policy_object_list_type: Policy Object ListType
        :returns: str
        """
        params = {
            "schemaType": schema_type,
            "policyObjectListType": policy_object_list_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectListType}/schema",
            return_type=str,
            params=params,
            **kw,
        )
