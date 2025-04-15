# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

TcpUdpProtocolValueDef = Literal["tcp", "udp"]

DefaultOptionTypeDef = Literal["default"]

EndpointTrackerTypeDef = Literal["static-route"]

DefaultEndpointTrackerTypeDef = Literal["static-route"]

TrackerTypeDef = Literal["endpoint"]

DefaultTrackerTypeDef = Literal["endpoint"]


@dataclass
class OneOfTrackerNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEndpointApiUrlOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEndpointApiUrlOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEndpointDnsNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEndpointDnsNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEndpointIpOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEndpointIpOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTrackerTcpUdpProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerTcpUdpProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # protocol type
    value: TcpUdpProtocolValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class EndpointTcpUdp:
    """
    Endpoint tcp/udp
    """

    port: Optional[Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2]] = _field(default=None)
    protocol: Optional[
        Union[OneOfTrackerTcpUdpProtocolOptionsDef1, OneOfTrackerTcpUdpProtocolOptionsDef2]
    ] = _field(default=None)


@dataclass
class OneOfIntervalOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMultiplierOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMultiplierOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMultiplierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfThresholdOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfThresholdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEndpointTrackerTypeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEndpointTrackerTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EndpointTrackerTypeDef


@dataclass
class OneOfEndpointTrackerTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultEndpointTrackerTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTrackerTypeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TrackerTypeDef


@dataclass
class OneOfTrackerTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultTrackerTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Data:
    tracker_name: Union[OneOfTrackerNameOptionsDef1, OneOfTrackerNameOptionsDef2] = _field(
        metadata={"alias": "trackerName"}
    )
    tracker_type: Union[
        OneOfTrackerTypeOptionsDef1, OneOfTrackerTypeOptionsDef2, OneOfTrackerTypeOptionsDef3
    ] = _field(metadata={"alias": "trackerType"})
    endpoint_api_url: Optional[
        Union[OneOfEndpointApiUrlOptionsDef1, OneOfEndpointApiUrlOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointApiUrl"})
    endpoint_dns_name: Optional[
        Union[OneOfEndpointDnsNameOptionsDef1, OneOfEndpointDnsNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointDnsName"})
    endpoint_ip: Optional[Union[OneOfEndpointIpOptionsDef1, OneOfEndpointIpOptionsDef2]] = _field(
        default=None, metadata={"alias": "endpointIp"}
    )
    # Endpoint tcp/udp
    endpoint_tcp_udp: Optional[EndpointTcpUdp] = _field(
        default=None, metadata={"alias": "endpointTcpUdp"}
    )
    endpoint_tracker_type: Optional[
        Union[
            OneOfEndpointTrackerTypeOptionsDef1,
            OneOfEndpointTrackerTypeOptionsDef2,
            OneOfEndpointTrackerTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "endpointTrackerType"})
    interval: Optional[
        Union[OneOfIntervalOptionsDef1, OneOfIntervalOptionsDef2, OneOfIntervalOptionsDef3]
    ] = _field(default=None)
    multiplier: Optional[
        Union[OneOfMultiplierOptionsDef1, OneOfMultiplierOptionsDef2, OneOfMultiplierOptionsDef3]
    ] = _field(default=None)
    threshold: Optional[
        Union[OneOfThresholdOptionsDef1, OneOfThresholdOptionsDef2, OneOfThresholdOptionsDef3]
    ] = _field(default=None)


@dataclass
class Payload:
    """
    Tracker profile parcel schema for common request
    """

    data: Data
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetLanVpnInterfaceEthernetAssociatedTrackerParcelsForTransportGetResponse:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # Tracker profile parcel schema for common request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetSingleSdwanServiceLanVpnInterfaceEthernetTrackerPayload:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # Tracker profile parcel schema for common request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPutRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateLanVpnInterfaceEthernetAndTrackerParcelAssociationForTransportPostRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)
