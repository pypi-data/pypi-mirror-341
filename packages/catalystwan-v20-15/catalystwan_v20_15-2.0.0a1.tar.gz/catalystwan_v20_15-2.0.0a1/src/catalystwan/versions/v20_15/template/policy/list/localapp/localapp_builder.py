# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .filtered.filtered_builder import FilteredBuilder
    from .preview.preview_builder import PreviewBuilder


class LocalappBuilder:
    """
    Builds and executes requests for operations under /template/policy/list/localapp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Create policy list
        POST /dataservice/template/policy/list/localapp

        :param payload: Policy list
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/list/localapp", payload=payload, **kw
        )

    def put(self, id: str, payload: Any, **kw) -> Any:
        """
        Edit policy list entries for a specific type of policy list
        PUT /dataservice/template/policy/list/localapp/{id}

        :param id: Policy Id
        :param payload: Policy list
        :returns: Any
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/policy/list/localapp/{id}",
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(self, id: str, **kw) -> Any:
        """
        Get a specific policy list based on the id
        GET /dataservice/template/policy/list/localapp/{id}

        :param id: Policy Id
        :returns: Any
        """
        ...

    @overload
    def get(self, **kw) -> List[Any]:
        """
        Get policy lists
        GET /dataservice/template/policy/list/localapp

        :returns: List[Any]
        """
        ...

    def get(self, id: Optional[str] = None, **kw) -> Union[List[Any], Any]:
        # /dataservice/template/policy/list/localapp/{id}
        if self._request_adapter.param_checker([(id, str)], []):
            params = {
                "id": id,
            }
            return self._request_adapter.request(
                "GET", "/dataservice/template/policy/list/localapp/{id}", params=params, **kw
            )
        # /dataservice/template/policy/list/localapp
        if self._request_adapter.param_checker([], [id]):
            return self._request_adapter.request(
                "GET", "/dataservice/template/policy/list/localapp", return_type=List[Any], **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def delete(self, *, id: str, **kw):
        """
        Delete policy list entry for a specific type of policy list
        DELETE /dataservice/template/policy/list/localapp/{id}

        :param id: Policy Id
        :returns: None
        """
        ...

    @overload
    def delete(self, *, info_tag: Optional[str] = None, **kw) -> List[Any]:
        """
        Delete policy lists with specific info tag
        DELETE /dataservice/template/policy/list/localapp

        :param info_tag: InfoTag
        :returns: List[Any]
        """
        ...

    def delete(
        self, *, info_tag: Optional[str] = None, id: Optional[str] = None, **kw
    ) -> Union[List[Any], None]:
        # /dataservice/template/policy/list/localapp/{id}
        if self._request_adapter.param_checker([(id, str)], [info_tag]):
            params = {
                "id": id,
            }
            return self._request_adapter.request(
                "DELETE", "/dataservice/template/policy/list/localapp/{id}", params=params, **kw
            )
        # /dataservice/template/policy/list/localapp
        if self._request_adapter.param_checker([], [id]):
            params = {
                "infoTag": info_tag,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/template/policy/list/localapp",
                return_type=List[Any],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def filtered(self) -> FilteredBuilder:
        """
        The filtered property
        """
        from .filtered.filtered_builder import FilteredBuilder

        return FilteredBuilder(self._request_adapter)

    @property
    def preview(self) -> PreviewBuilder:
        """
        The preview property
        """
        from .preview.preview_builder import PreviewBuilder

        return PreviewBuilder(self._request_adapter)
