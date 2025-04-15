# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

ConnectivityGatewayTypeParam = Literal[
    "DIRECT_CONNECT_GATEWAY",
    "EXPRESS_ROUTE_CIRCUIT",
    "GCR_ATTACHMENT",
    "TRANSIT_GATEWAY",
    "VIRTUAL_INTERFACES",
    "VIRTUAL_PRIVATE_GATEWAY",
]


@dataclass
class InlineResponse20014CreationOptionsExpressRouteCircuitServiceProviderList:
    bandwidths_offered: Optional[List[int]] = _field(
        default=None, metadata={"alias": "bandwidthsOffered"}
    )
    id: Optional[str] = _field(default=None)
    location: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    peering_locations: Optional[List[str]] = _field(
        default=None, metadata={"alias": "peeringLocations"}
    )
    # Provisioning state of the resource
    provisioning_state: Optional[str] = _field(
        default=None, metadata={"alias": "provisioningState"}
    )
    # Type of Resource
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class InlineResponse20014CreationOptionsResourceGroupList:
    id: Optional[str] = _field(default=None)
    location: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class InlineResponse20014CreationOptions:
    express_route_circuit_service_provider_list: Optional[
        List[InlineResponse20014CreationOptionsExpressRouteCircuitServiceProviderList]
    ] = _field(default=None, metadata={"alias": "expressRouteCircuitServiceProviderList"})
    resource_group_list: Optional[List[InlineResponse20014CreationOptionsResourceGroupList]] = (
        _field(default=None, metadata={"alias": "resourceGroupList"})
    )


@dataclass
class InlineResponse20014:
    creation_options: Optional[InlineResponse20014CreationOptions] = _field(
        default=None, metadata={"alias": "creationOptions"}
    )
