# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]


@dataclass
class CreateNfvirtualSystemSettingsParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfNameServerNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNameServerNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class NameServer:
    name: Union[OneOfNameServerNameOptionsDef1, OneOfNameServerNameOptionsDef2]


@dataclass
class OneOfDpdkOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDpdkOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[bool] = _field(default=None)


@dataclass
class Data:
    dpdk: Optional[Union[OneOfDpdkOptionsDef1, OneOfDpdkOptionsDef2]] = _field(default=None)
    # Name Server
    name_server: Optional[List[NameServer]] = _field(default=None, metadata={"alias": "nameServer"})


@dataclass
class CreateNfvirtualSystemSettingsParcelPostRequest:
    """
    SystemSettings profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class SystemSettingsOneOfNameServerNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSettingsNameServer:
    name: Union[SystemSettingsOneOfNameServerNameOptionsDef1, OneOfNameServerNameOptionsDef2]


@dataclass
class SystemSettingsData:
    dpdk: Optional[Union[OneOfDpdkOptionsDef1, OneOfDpdkOptionsDef2]] = _field(default=None)
    # Name Server
    name_server: Optional[List[SystemSettingsNameServer]] = _field(
        default=None, metadata={"alias": "nameServer"}
    )


@dataclass
class Payload:
    """
    SystemSettings profile parcel schema for PUT request
    """

    data: SystemSettingsData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualSystemSystemSettingsPayload:
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
    # SystemSettings profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditNfvirtualSystemSettingsParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemSystemSettingsOneOfNameServerNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSystemSettingsNameServer:
    name: Union[SystemSystemSettingsOneOfNameServerNameOptionsDef1, OneOfNameServerNameOptionsDef2]


@dataclass
class SystemSystemSettingsData:
    dpdk: Optional[Union[OneOfDpdkOptionsDef1, OneOfDpdkOptionsDef2]] = _field(default=None)
    # Name Server
    name_server: Optional[List[SystemSystemSettingsNameServer]] = _field(
        default=None, metadata={"alias": "nameServer"}
    )


@dataclass
class EditNfvirtualSystemSettingsParcelPutRequest:
    """
    SystemSettings profile parcel schema for PUT request
    """

    data: SystemSystemSettingsData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
