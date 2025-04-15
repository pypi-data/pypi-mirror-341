# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

SeverityDef = Literal[
    "alert", "critical", "debug", "emergency", "error", "information", "notice", "warn"
]

DefaultOptionTypeDef = Literal["default"]

DefaultSeverityDef = Literal["information"]

LoggingSeverityDef = Literal[
    "alert", "critical", "debug", "emergency", "error", "information", "notice", "warn"
]

LoggingDefaultSeverityDef = Literal["information"]

SystemLoggingSeverityDef = Literal[
    "alert", "critical", "debug", "emergency", "error", "information", "notice", "warn"
]

SystemLoggingDefaultSeverityDef = Literal["information"]


@dataclass
class CreateNfvirtualLoggingParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfHostIpAddressNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfHostIpAddressNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class HostIpAddress:
    name: Union[OneOfHostIpAddressNameOptionsDef1, OneOfHostIpAddressNameOptionsDef2]


@dataclass
class OneOfSeverityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SeverityDef


@dataclass
class OneOfSeverityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSeverityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[DefaultSeverityDef] = _field(default=None)


@dataclass
class Data:
    # Enable logging to remote server
    host_ip_address: Optional[List[HostIpAddress]] = _field(
        default=None, metadata={"alias": "host-ip-address"}
    )
    severity: Optional[
        Union[OneOfSeverityOptionsDef1, OneOfSeverityOptionsDef2, OneOfSeverityOptionsDef3]
    ] = _field(default=None)


@dataclass
class CreateNfvirtualLoggingParcelPostRequest:
    """
    Logging profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class LoggingOneOfHostIpAddressNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LoggingHostIpAddress:
    name: Union[LoggingOneOfHostIpAddressNameOptionsDef1, OneOfHostIpAddressNameOptionsDef2]


@dataclass
class LoggingOneOfSeverityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LoggingSeverityDef


@dataclass
class LoggingOneOfSeverityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[LoggingDefaultSeverityDef] = _field(default=None)


@dataclass
class LoggingData:
    # Enable logging to remote server
    host_ip_address: Optional[List[LoggingHostIpAddress]] = _field(
        default=None, metadata={"alias": "host-ip-address"}
    )
    severity: Optional[
        Union[
            LoggingOneOfSeverityOptionsDef1,
            OneOfSeverityOptionsDef2,
            LoggingOneOfSeverityOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Payload:
    """
    Logging profile parcel schema for PUT request
    """

    data: LoggingData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualSystemLoggingPayload:
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
    # Logging profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditNfvirtualLoggingParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemLoggingOneOfHostIpAddressNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemLoggingHostIpAddress:
    name: Union[SystemLoggingOneOfHostIpAddressNameOptionsDef1, OneOfHostIpAddressNameOptionsDef2]


@dataclass
class SystemLoggingOneOfSeverityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemLoggingSeverityDef


@dataclass
class SystemLoggingOneOfSeverityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[SystemLoggingDefaultSeverityDef] = _field(default=None)


@dataclass
class SystemLoggingData:
    # Enable logging to remote server
    host_ip_address: Optional[List[SystemLoggingHostIpAddress]] = _field(
        default=None, metadata={"alias": "host-ip-address"}
    )
    severity: Optional[
        Union[
            SystemLoggingOneOfSeverityOptionsDef1,
            OneOfSeverityOptionsDef2,
            SystemLoggingOneOfSeverityOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class EditNfvirtualLoggingParcelPutRequest:
    """
    Logging profile parcel schema for PUT request
    """

    data: SystemLoggingData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
