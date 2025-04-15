# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

Value = Literal["systemIp"]

VariableOptionTypeDef = Literal["variable"]

LoggingValue = Literal["{{logging_server_source_ip}}"]

PrioritytDef = Literal["alert", "critical", "emergency", "error", "information", "notice", "warn"]

GlobalLoggingValue = Literal["error"]

LoggingPrioritytDef = Literal[
    "alert", "critical", "emergency", "error", "information", "notice", "warn"
]

GlobalLoggingPrioritytDef = Literal[
    "alert", "critical", "emergency", "error", "information", "notice", "warn"
]


@dataclass
class OneOfDiskFileSizeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDiskFileSizeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDiskFileRotateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDiskFileRotateOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class File:
    """
    File to which to log messages
    """

    disk_file_rotate: Union[OneOfDiskFileRotateOptionsDef1, OneOfDiskFileRotateOptionsDef2] = (
        _field(metadata={"alias": "diskFileRotate"})
    )
    disk_file_size: Union[OneOfDiskFileSizeOptionsDef1, OneOfDiskFileSizeOptionsDef2] = _field(
        metadata={"alias": "diskFileSize"}
    )


@dataclass
class Disk:
    """
    Enable logging to disk
    """

    # File to which to log messages
    file: File


@dataclass
class OneOfServerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfsourceIpOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfsourceIpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LoggingValue  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PrioritytDef


@dataclass
class OneOfPriorityOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalLoggingValue  # pytype: disable=annotation-type-mismatch


@dataclass
class Server:
    name: OneOfServerNameOptionsDef
    priority: Union[OneOfPriorityOptionsDef1, OneOfPriorityOptionsDef2]
    source_ip: Union[OneOfsourceIpOptionsDef1, OneOfsourceIpOptionsDef2] = _field(
        metadata={"alias": "sourceIp"}
    )


@dataclass
class LoggingData:
    # Enable logging to disk
    disk: Disk
    # Remote host logging parameters
    server: Optional[List[Server]] = _field(default=None)


@dataclass
class Payload:
    """
    Logging profile parcel schema for POST request
    """

    data: LoggingData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


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
    # Logging profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListMobilityGlobalLoggingPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateLoggingProfileFeatureForMobilityPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalLoggingData:
    # Enable logging to disk
    disk: Disk
    # Remote host logging parameters
    server: Optional[List[Server]] = _field(default=None)


@dataclass
class CreateLoggingProfileFeatureForMobilityPostRequest:
    """
    Logging profile parcel schema for POST request
    """

    data: GlobalLoggingData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class LoggingOneOfDiskFileSizeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LoggingOneOfDiskFileRotateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LoggingFile:
    """
    File to which to log messages
    """

    disk_file_rotate: Union[
        LoggingOneOfDiskFileRotateOptionsDef1, OneOfDiskFileRotateOptionsDef2
    ] = _field(metadata={"alias": "diskFileRotate"})
    disk_file_size: Union[LoggingOneOfDiskFileSizeOptionsDef1, OneOfDiskFileSizeOptionsDef2] = (
        _field(metadata={"alias": "diskFileSize"})
    )


@dataclass
class LoggingDisk:
    """
    Enable logging to disk
    """

    # File to which to log messages
    file: LoggingFile


@dataclass
class LoggingOneOfServerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LoggingOneOfPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LoggingPrioritytDef


@dataclass
class LoggingServer:
    name: LoggingOneOfServerNameOptionsDef
    priority: Union[LoggingOneOfPriorityOptionsDef1, OneOfPriorityOptionsDef2]
    source_ip: Union[OneOfsourceIpOptionsDef1, OneOfsourceIpOptionsDef2] = _field(
        metadata={"alias": "sourceIp"}
    )


@dataclass
class MobilityGlobalLoggingData:
    # Enable logging to disk
    disk: LoggingDisk
    # Remote host logging parameters
    server: Optional[List[LoggingServer]] = _field(default=None)


@dataclass
class LoggingPayload:
    """
    Logging profile parcel schema for PUT request
    """

    data: MobilityGlobalLoggingData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleMobilityGlobalLoggingPayload:
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
    payload: Optional[LoggingPayload] = _field(default=None)


@dataclass
class EditLoggingProfileFeatureForMobilityPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalLoggingOneOfDiskFileSizeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalLoggingOneOfDiskFileRotateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalLoggingFile:
    """
    File to which to log messages
    """

    disk_file_rotate: Union[
        GlobalLoggingOneOfDiskFileRotateOptionsDef1, OneOfDiskFileRotateOptionsDef2
    ] = _field(metadata={"alias": "diskFileRotate"})
    disk_file_size: Union[
        GlobalLoggingOneOfDiskFileSizeOptionsDef1, OneOfDiskFileSizeOptionsDef2
    ] = _field(metadata={"alias": "diskFileSize"})


@dataclass
class GlobalLoggingDisk:
    """
    Enable logging to disk
    """

    # File to which to log messages
    file: GlobalLoggingFile


@dataclass
class GlobalLoggingOneOfServerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalLoggingOneOfPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalLoggingPrioritytDef


@dataclass
class GlobalLoggingServer:
    name: GlobalLoggingOneOfServerNameOptionsDef
    priority: Union[GlobalLoggingOneOfPriorityOptionsDef1, OneOfPriorityOptionsDef2]
    source_ip: Union[OneOfsourceIpOptionsDef1, OneOfsourceIpOptionsDef2] = _field(
        metadata={"alias": "sourceIp"}
    )


@dataclass
class FeatureProfileMobilityGlobalLoggingData:
    # Enable logging to disk
    disk: GlobalLoggingDisk
    # Remote host logging parameters
    server: Optional[List[GlobalLoggingServer]] = _field(default=None)


@dataclass
class EditLoggingProfileFeatureForMobilityPutRequest:
    """
    Logging profile parcel schema for PUT request
    """

    data: FeatureProfileMobilityGlobalLoggingData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
