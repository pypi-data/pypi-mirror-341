# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateThousandeyesProfileParcelForOtherPostRequest,
    CreateThousandeyesProfileParcelForOtherPostResponse,
    EditThousandeyesProfileParcelForOtherPutRequest,
    EditThousandeyesProfileParcelForOtherPutResponse,
    GetListSdwanOtherThousandeyesPayload,
    GetSingleSdwanOtherThousandeyesPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class ThousandeyesBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/other/thousandeyes
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, other_id: str, payload: CreateThousandeyesProfileParcelForOtherPostRequest, **kw
    ) -> CreateThousandeyesProfileParcelForOtherPostResponse:
        """
        Create a Thousandeyes Profile Parcel for Other feature profile
        POST /dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes

        :param other_id: Feature Profile ID
        :param payload: Thousandeyes Profile Parcel
        :returns: CreateThousandeyesProfileParcelForOtherPostResponse
        """
        params = {
            "otherId": other_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes",
            return_type=CreateThousandeyesProfileParcelForOtherPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        other_id: str,
        thousandeyes_id: str,
        payload: EditThousandeyesProfileParcelForOtherPutRequest,
        **kw,
    ) -> EditThousandeyesProfileParcelForOtherPutResponse:
        """
        Update a Thousandeyes Profile Parcel for Other feature profile
        PUT /dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes/{thousandeyesId}

        :param other_id: Feature Profile ID
        :param thousandeyes_id: Profile Parcel ID
        :param payload: Thousandeyes Profile Parcel
        :returns: EditThousandeyesProfileParcelForOtherPutResponse
        """
        params = {
            "otherId": other_id,
            "thousandeyesId": thousandeyes_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes/{thousandeyesId}",
            return_type=EditThousandeyesProfileParcelForOtherPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, other_id: str, thousandeyes_id: str, **kw):
        """
        Delete a Thousandeyes Profile Parcel for Other feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes/{thousandeyesId}

        :param other_id: Feature Profile ID
        :param thousandeyes_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "otherId": other_id,
            "thousandeyesId": thousandeyes_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes/{thousandeyesId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, other_id: str, thousandeyes_id: str, **kw
    ) -> GetSingleSdwanOtherThousandeyesPayload:
        """
        Get Thousandeyes Profile Parcel by parcelId for Other feature profile
        GET /dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes/{thousandeyesId}

        :param other_id: Feature Profile ID
        :param thousandeyes_id: Profile Parcel ID
        :returns: GetSingleSdwanOtherThousandeyesPayload
        """
        ...

    @overload
    def get(self, other_id: str, **kw) -> GetListSdwanOtherThousandeyesPayload:
        """
        Get Thousandeyes Profile Parcels for Other feature profile
        GET /dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes

        :param other_id: Feature Profile ID
        :returns: GetListSdwanOtherThousandeyesPayload
        """
        ...

    def get(
        self, other_id: str, thousandeyes_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanOtherThousandeyesPayload, GetSingleSdwanOtherThousandeyesPayload]:
        # /dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes/{thousandeyesId}
        if self._request_adapter.param_checker([(other_id, str), (thousandeyes_id, str)], []):
            params = {
                "otherId": other_id,
                "thousandeyesId": thousandeyes_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes/{thousandeyesId}",
                return_type=GetSingleSdwanOtherThousandeyesPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes
        if self._request_adapter.param_checker([(other_id, str)], [thousandeyes_id]):
            params = {
                "otherId": other_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/other/{otherId}/thousandeyes",
                return_type=GetListSdwanOtherThousandeyesPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
