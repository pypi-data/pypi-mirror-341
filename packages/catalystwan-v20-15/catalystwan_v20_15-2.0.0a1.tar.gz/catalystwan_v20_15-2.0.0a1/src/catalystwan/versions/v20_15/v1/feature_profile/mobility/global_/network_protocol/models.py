# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

Type = Literal[
    "cellular", "ethernet", "globalSettings", "networkProtocol", "securityPolicy", "wifi"
]


@dataclass
class Variable:
    json_path: str = _field(metadata={"alias": "jsonPath"})
    var_name: str = _field(metadata={"alias": "varName"})


@dataclass
class DhcpPool:
    lease_time_day: int = _field(metadata={"alias": "leaseTimeDay"})
    lease_time_hour: int = _field(metadata={"alias": "leaseTimeHour"})
    lease_time_min: int = _field(metadata={"alias": "leaseTimeMin"})
    pool_network: str = _field(metadata={"alias": "poolNetwork"})


@dataclass
class NatRule:
    description: str
    in_port: int = _field(metadata={"alias": "inPort"})
    inside_ip: str = _field(metadata={"alias": "insideIp"})
    interface: str
    out_port: int = _field(metadata={"alias": "outPort"})
    protocol: str


@dataclass
class NetworkProtocol:
    # Name of the Profile Parcel. Must be unique.
    name: str
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    dhcp_pool: Optional[DhcpPool] = _field(default=None, metadata={"alias": "DHCPPool"})
    dns_settings: Optional[str] = _field(default=None, metadata={"alias": "DNSSettings"})
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    nat_rules: Optional[List[NatRule]] = _field(default=None, metadata={"alias": "NATRules"})
    ntp_inherit: Optional[bool] = _field(default=None, metadata={"alias": "NTPInherit"})
    ntp_settings: Optional[List[str]] = _field(default=None, metadata={"alias": "NTPSettings"})
    variables: Optional[List[Variable]] = _field(default=None)


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
    payload: Optional[NetworkProtocol] = _field(default=None)


@dataclass
class GetListMobilityGlobalNetworkprotocolPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateNetworkProtocolProfileParcelForMobilityPostRequest:
    # Name of the Profile Parcel. Must be unique.
    name: str
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    dhcp_pool: Optional[DhcpPool] = _field(default=None, metadata={"alias": "DHCPPool"})
    dns_settings: Optional[str] = _field(default=None, metadata={"alias": "DNSSettings"})
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    nat_rules: Optional[List[NatRule]] = _field(default=None, metadata={"alias": "NATRules"})
    ntp_inherit: Optional[bool] = _field(default=None, metadata={"alias": "NTPInherit"})
    ntp_settings: Optional[List[str]] = _field(default=None, metadata={"alias": "NTPSettings"})
    variables: Optional[List[Variable]] = _field(default=None)


@dataclass
class GetSingleMobilityGlobalNetworkprotocolPayload:
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
    payload: Optional[NetworkProtocol] = _field(default=None)


@dataclass
class EditNetworkProtocolProfileParcelForMobilityPutRequest:
    # Name of the Profile Parcel. Must be unique.
    name: str
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    dhcp_pool: Optional[DhcpPool] = _field(default=None, metadata={"alias": "DHCPPool"})
    dns_settings: Optional[str] = _field(default=None, metadata={"alias": "DNSSettings"})
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    nat_rules: Optional[List[NatRule]] = _field(default=None, metadata={"alias": "NATRules"})
    ntp_inherit: Optional[bool] = _field(default=None, metadata={"alias": "NTPInherit"})
    ntp_settings: Optional[List[str]] = _field(default=None, metadata={"alias": "NTPSettings"})
    variables: Optional[List[Variable]] = _field(default=None)
