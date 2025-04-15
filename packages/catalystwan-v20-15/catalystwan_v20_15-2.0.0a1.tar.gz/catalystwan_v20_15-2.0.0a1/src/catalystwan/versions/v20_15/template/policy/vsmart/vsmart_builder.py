# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .activate.activate_builder import ActivateBuilder
    from .central.central_builder import CentralBuilder
    from .connectivity.connectivity_builder import ConnectivityBuilder
    from .deactivate.deactivate_builder import DeactivateBuilder
    from .definition.definition_builder import DefinitionBuilder
    from .qosmos_nbar_migration_warning.qosmos_nbar_migration_warning_builder import (
        QosmosNbarMigrationWarningBuilder,
    )


class VsmartBuilder:
    """
    Builds and executes requests for operations under /template/policy/vsmart
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get all template vsmart policy list
        GET /dataservice/template/policy/vsmart

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/policy/vsmart", return_type=List[Any], **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Create template for given policy
        POST /dataservice/template/policy/vsmart

        :param payload: Template policy
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/vsmart", payload=payload, **kw
        )

    def put(self, policy_id: str, payload: Any, **kw) -> List[Any]:
        """
        Edit template for given policy id
        PUT /dataservice/template/policy/vsmart/{policyId}

        :param policy_id: Policy Id
        :param payload: Template policy
        :returns: List[Any]
        """
        params = {
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/policy/vsmart/{policyId}",
            return_type=List[Any],
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, policy_id: str, **kw):
        """
        Delete template for a given policy id
        DELETE /dataservice/template/policy/vsmart/{policyId}

        :param policy_id: Policy Id
        :returns: None
        """
        params = {
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/template/policy/vsmart/{policyId}", params=params, **kw
        )

    @property
    def activate(self) -> ActivateBuilder:
        """
        The activate property
        """
        from .activate.activate_builder import ActivateBuilder

        return ActivateBuilder(self._request_adapter)

    @property
    def central(self) -> CentralBuilder:
        """
        The central property
        """
        from .central.central_builder import CentralBuilder

        return CentralBuilder(self._request_adapter)

    @property
    def connectivity(self) -> ConnectivityBuilder:
        """
        The connectivity property
        """
        from .connectivity.connectivity_builder import ConnectivityBuilder

        return ConnectivityBuilder(self._request_adapter)

    @property
    def deactivate(self) -> DeactivateBuilder:
        """
        The deactivate property
        """
        from .deactivate.deactivate_builder import DeactivateBuilder

        return DeactivateBuilder(self._request_adapter)

    @property
    def definition(self) -> DefinitionBuilder:
        """
        The definition property
        """
        from .definition.definition_builder import DefinitionBuilder

        return DefinitionBuilder(self._request_adapter)

    @property
    def qosmos_nbar_migration_warning(self) -> QosmosNbarMigrationWarningBuilder:
        """
        The qosmos_nbar_migration_warning property
        """
        from .qosmos_nbar_migration_warning.qosmos_nbar_migration_warning_builder import (
            QosmosNbarMigrationWarningBuilder,
        )

        return QosmosNbarMigrationWarningBuilder(self._request_adapter)
