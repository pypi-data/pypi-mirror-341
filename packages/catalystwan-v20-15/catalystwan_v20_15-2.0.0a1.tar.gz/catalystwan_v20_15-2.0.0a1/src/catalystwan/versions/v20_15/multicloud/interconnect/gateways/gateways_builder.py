# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectGatewayExtended, InterconnectTypeParam, ProcessResponse

if TYPE_CHECKING:
    from .config_group.config_group_builder import ConfigGroupBuilder
    from .device_chassis_numbers.device_chassis_numbers_builder import DeviceChassisNumbersBuilder
    from .devices.devices_builder import DevicesBuilder
    from .image_names.image_names_builder import ImageNamesBuilder
    from .instance_sizes.instance_sizes_builder import InstanceSizesBuilder
    from .push_config.push_config_builder import PushConfigBuilder
    from .settings.settings_builder import SettingsBuilder
    from .types.types_builder import TypesBuilder


class GatewaysBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/gateways
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get_list(
        self,
        interconnect_type: Optional[InterconnectTypeParam] = None,
        interconnect_account_id: Optional[str] = None,
        region: Optional[str] = None,
        region_id: Optional[str] = None,
        interconnect_gateway_name: Optional[str] = None,
        resource_state: Optional[str] = None,
        interconnect_billing_account_id: Optional[str] = None,
        refresh: Optional[str] = "false",
        **kw,
    ) -> List[InterconnectGatewayExtended]:
        """
        API to retrieve all Interconnect Gateways from vManage.
        GET /dataservice/multicloud/interconnect/gateways

        :param interconnect_type: Interconnect provider type
        :param interconnect_account_id: Interconnect provider account id
        :param region: Interconnect Region
        :param region_id: Interconnect Region Id
        :param interconnect_gateway_name: Interconnect Gateway Name
        :param resource_state: Interconnect Resource State
        :param interconnect_billing_account_id: Interconnect Billing Account Id
        :param refresh: Refresh
        :returns: List[InterconnectGatewayExtended]
        """
        params = {
            "interconnect-type": interconnect_type,
            "interconnect-account-id": interconnect_account_id,
            "region": region,
            "region-id": region_id,
            "interconnect-gateway-name": interconnect_gateway_name,
            "resource-state": resource_state,
            "interconnect-billing-account-id": interconnect_billing_account_id,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/gateways",
            return_type=List[InterconnectGatewayExtended],
            params=params,
            **kw,
        )

    def post(self, payload: InterconnectGatewayExtended, **kw) -> ProcessResponse:
        """
        API to create an Intercoonect gateway in an Interconnect provider.
        POST /dataservice/multicloud/interconnect/gateways

        :param payload: Request Payload for Multicloud Interconnect Gateways
        :returns: ProcessResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/interconnect/gateways",
            return_type=ProcessResponse,
            payload=payload,
            **kw,
        )

    def get(self, interconnect_gateway_name: str, **kw) -> InterconnectGatewayExtended:
        """
        API to retrieve the Interconnect Gateway Information from vManage.
        GET /dataservice/multicloud/interconnect/gateways/{interconnect-gateway-name}

        :param interconnect_gateway_name: Interconnect gateway name
        :returns: InterconnectGatewayExtended
        """
        params = {
            "interconnect-gateway-name": interconnect_gateway_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/gateways/{interconnect-gateway-name}",
            return_type=InterconnectGatewayExtended,
            params=params,
            **kw,
        )

    def put(
        self, interconnect_gateway_name: str, payload: InterconnectGatewayExtended, **kw
    ) -> InterconnectGatewayExtended:
        """
        API to update the Interconnect Gateway Information in vManage.
        PUT /dataservice/multicloud/interconnect/gateways/{interconnect-gateway-name}

        :param interconnect_gateway_name: Interconnect gateway name
        :param payload: Request Payload for Multicloud Interconnect Gateways
        :returns: InterconnectGatewayExtended
        """
        params = {
            "interconnect-gateway-name": interconnect_gateway_name,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/interconnect/gateways/{interconnect-gateway-name}",
            return_type=InterconnectGatewayExtended,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, interconnect_gateway_name: str, **kw) -> ProcessResponse:
        """
        API to delete an Interconnect Gateway from an Interconnect provider.
        DELETE /dataservice/multicloud/interconnect/gateways/{interconnect-gateway-name}

        :param interconnect_gateway_name: Interconnect gateway name
        :returns: ProcessResponse
        """
        params = {
            "interconnect-gateway-name": interconnect_gateway_name,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/interconnect/gateways/{interconnect-gateway-name}",
            return_type=ProcessResponse,
            params=params,
            **kw,
        )

    @property
    def config_group(self) -> ConfigGroupBuilder:
        """
        The config-group property
        """
        from .config_group.config_group_builder import ConfigGroupBuilder

        return ConfigGroupBuilder(self._request_adapter)

    @property
    def device_chassis_numbers(self) -> DeviceChassisNumbersBuilder:
        """
        The device-chassis-numbers property
        """
        from .device_chassis_numbers.device_chassis_numbers_builder import (
            DeviceChassisNumbersBuilder,
        )

        return DeviceChassisNumbersBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)

    @property
    def image_names(self) -> ImageNamesBuilder:
        """
        The image-names property
        """
        from .image_names.image_names_builder import ImageNamesBuilder

        return ImageNamesBuilder(self._request_adapter)

    @property
    def instance_sizes(self) -> InstanceSizesBuilder:
        """
        The instance-sizes property
        """
        from .instance_sizes.instance_sizes_builder import InstanceSizesBuilder

        return InstanceSizesBuilder(self._request_adapter)

    @property
    def push_config(self) -> PushConfigBuilder:
        """
        The push-config property
        """
        from .push_config.push_config_builder import PushConfigBuilder

        return PushConfigBuilder(self._request_adapter)

    @property
    def settings(self) -> SettingsBuilder:
        """
        The settings property
        """
        from .settings.settings_builder import SettingsBuilder

        return SettingsBuilder(self._request_adapter)

    @property
    def types(self) -> TypesBuilder:
        """
        The types property
        """
        from .types.types_builder import TypesBuilder

        return TypesBuilder(self._request_adapter)
