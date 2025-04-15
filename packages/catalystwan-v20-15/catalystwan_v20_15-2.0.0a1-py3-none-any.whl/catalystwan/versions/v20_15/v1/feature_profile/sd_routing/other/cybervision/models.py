# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

Ipv4SubnetMaskDef = Literal[
    "0.0.0.0",
    "128.0.0.0",
    "192.0.0.0",
    "224.0.0.0",
    "240.0.0.0",
    "248.0.0.0",
    "252.0.0.0",
    "254.0.0.0",
    "255.0.0.0",
    "255.128.0.0",
    "255.192.0.0",
    "255.224.0.0",
    "255.240.0.0",
    "255.252.0.0",
    "255.254.0.0",
    "255.255.0.0",
    "255.255.128.0",
    "255.255.192.0",
    "255.255.224.0",
    "255.255.240.0",
    "255.255.248.0",
    "255.255.252.0",
    "255.255.254.0",
    "255.255.255.0",
    "255.255.255.128",
    "255.255.255.192",
    "255.255.255.224",
    "255.255.255.240",
    "255.255.255.248",
    "255.255.255.252",
    "255.255.255.254",
    "255.255.255.255",
]


@dataclass
class OneOfVirtualApplicationcaptureInterfaceIpDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfVirtualApplicationcaptureInterfaceIpDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVirtualApplicationIngressIfSubnetMaskDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVirtualApplicationIngressIfSubnetMaskDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVirtualApplicationcollectionInterfaceIpDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfVirtualApplicationcollectionInterfaceIpDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVirtualApplicationcollectionInterfaceSubnetMask1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVirtualApplicationcollectionInterfaceSubnetMask2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class MultipleErspanSourceInterfaces:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVirtualApplicationvirtualPortGroup5IpDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfVirtualApplicationvirtualPortGroup5IpDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVirtualApplicationvirtualPortGroup6IpDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfVirtualApplicationvirtualPortGroup6IpDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVirtualApplicationerspanSourceInterfaceDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfcvcId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VirtualApplication:
    """
    Virtual application Instance
    """

    capture_interface_ip: Union[
        OneOfVirtualApplicationcaptureInterfaceIpDef1, OneOfVirtualApplicationcaptureInterfaceIpDef2
    ] = _field(metadata={"alias": "captureInterfaceIP"})
    capture_interface_subnet_mask: Union[
        OneOfVirtualApplicationIngressIfSubnetMaskDef1,
        OneOfVirtualApplicationIngressIfSubnetMaskDef2,
    ] = _field(metadata={"alias": "captureInterfaceSubnetMask"})
    collection_interface_ip: Union[
        OneOfVirtualApplicationcollectionInterfaceIpDef1,
        OneOfVirtualApplicationcollectionInterfaceIpDef2,
    ] = _field(metadata={"alias": "collectionInterfaceIP"})
    collection_interface_subnet_mask: Union[
        OneOfVirtualApplicationcollectionInterfaceSubnetMask1,
        OneOfVirtualApplicationcollectionInterfaceSubnetMask2,
    ] = _field(metadata={"alias": "collectionInterfaceSubnetMask"})
    cvc_id: OneOfcvcId = _field(metadata={"alias": "cvcId"})
    multiple_erspan_source_interfaces: List[MultipleErspanSourceInterfaces] = _field(
        metadata={"alias": "multipleErspanSourceInterfaces"}
    )
    sensor_to_cvc_interface: OneOfVirtualApplicationerspanSourceInterfaceDef = _field(
        metadata={"alias": "sensorToCvcInterface"}
    )
    virtual_port_group5_ip: Union[
        OneOfVirtualApplicationvirtualPortGroup5IpDef1,
        OneOfVirtualApplicationvirtualPortGroup5IpDef2,
    ] = _field(metadata={"alias": "virtualPortGroup5Ip"})
    virtual_port_group6_ip: Union[
        OneOfVirtualApplicationvirtualPortGroup6IpDef1,
        OneOfVirtualApplicationvirtualPortGroup6IpDef2,
    ] = _field(metadata={"alias": "virtualPortGroup6Ip"})


@dataclass
class CybervisionData:
    # Virtual application Instance
    virtual_application: VirtualApplication = _field(metadata={"alias": "virtualApplication"})


@dataclass
class Payload:
    """
    cybervision profile feature schema for POST/PUT request
    """

    data: CybervisionData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class Data:
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
    # cybervision profile feature schema for POST/PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingOtherCybervisionPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateCybervisionProfileFeatureForOtherPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OtherCybervisionData:
    # Virtual application Instance
    virtual_application: VirtualApplication = _field(metadata={"alias": "virtualApplication"})


@dataclass
class CreateCybervisionProfileFeatureForOtherPostRequest:
    """
    cybervision profile feature schema for POST/PUT request
    """

    data: OtherCybervisionData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdRoutingOtherCybervisionPayload:
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
    # cybervision profile feature schema for POST/PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditCybervisionProfileFeatureForOtherPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingOtherCybervisionData:
    # Virtual application Instance
    virtual_application: VirtualApplication = _field(metadata={"alias": "virtualApplication"})


@dataclass
class EditCybervisionProfileFeatureForOtherPutRequest:
    """
    cybervision profile feature schema for POST/PUT request
    """

    data: SdRoutingOtherCybervisionData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
