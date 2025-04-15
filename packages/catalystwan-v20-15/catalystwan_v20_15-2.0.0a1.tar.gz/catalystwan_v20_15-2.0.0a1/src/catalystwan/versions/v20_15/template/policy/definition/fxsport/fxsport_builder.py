# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, overload

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .bulk.bulk_builder import BulkBuilder
    from .multiple.multiple_builder import MultipleBuilder
    from .preview.preview_builder import PreviewBuilder


class FxsportBuilder:
    """
    Builds and executes requests for operations under /template/policy/definition/fxsport
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Create policy definition
        POST /dataservice/template/policy/definition/fxsport

        :param payload: Policy definition
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/definition/fxsport", payload=payload, **kw
        )

    def put(self, id: str, payload: Any, **kw) -> Any:
        """
        Edit a policy definitions
        PUT /dataservice/template/policy/definition/fxsport/{id}

        :param id: Policy Id
        :param payload: Policy definition
        :returns: Any
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/policy/definition/fxsport/{id}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, id: str, **kw):
        """
        Delete policy definition
        DELETE /dataservice/template/policy/definition/fxsport/{id}

        :param id: Policy Id
        :returns: None
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/template/policy/definition/fxsport/{id}", params=params, **kw
        )

    @overload
    def get(self, id: str, **kw) -> Any:
        """
        Get a specific policy definitions
        GET /dataservice/template/policy/definition/fxsport/{id}

        :param id: Policy Id
        :returns: Any
        """
        ...

    @overload
    def get(self, **kw) -> Any:
        """
        Get policy definitions
        GET /dataservice/template/policy/definition/fxsport

        :returns: Any
        """
        ...

    def get(self, id: Optional[str] = None, **kw) -> Any:
        # /dataservice/template/policy/definition/fxsport/{id}
        if self._request_adapter.param_checker([(id, str)], []):
            params = {
                "id": id,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/template/policy/definition/fxsport/{id}", params=params, **kw
            )
        # /dataservice/template/policy/definition/fxsport
        if self._request_adapter.param_checker([], [id]):
            return self._request_adapter.request(
                "GET", "/dataservice/template/policy/definition/fxsport", **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def bulk(self) -> BulkBuilder:
        """
        The bulk property
        """
        from .bulk.bulk_builder import BulkBuilder

        return BulkBuilder(self._request_adapter)

    @property
    def multiple(self) -> MultipleBuilder:
        """
        The multiple property
        """
        from .multiple.multiple_builder import MultipleBuilder

        return MultipleBuilder(self._request_adapter)

    @property
    def preview(self) -> PreviewBuilder:
        """
        The preview property
        """
        from .preview.preview_builder import PreviewBuilder

        return PreviewBuilder(self._request_adapter)
