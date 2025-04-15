# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

EmptyStringDef = Literal[""]


@dataclass
class OneOfOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EmptyStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class BannerData:
    login: Union[OneOfOptionsDef1, OneOfOptionsDef2, OneOfOptionsDef3]
    motd: Union[OneOfOptionsDef1, OneOfOptionsDef2, OneOfOptionsDef3]


@dataclass
class Payload:
    """
    Banner profile parcel schema for POST request
    """

    data: BannerData
    name: str
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
    # Banner profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSystemBannerPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateBannerProfileParcelForSystemPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemBannerData:
    login: Union[OneOfOptionsDef1, OneOfOptionsDef2, OneOfOptionsDef3]
    motd: Union[OneOfOptionsDef1, OneOfOptionsDef2, OneOfOptionsDef3]


@dataclass
class CreateBannerProfileParcelForSystemPostRequest:
    """
    Banner profile parcel schema for POST request
    """

    data: SystemBannerData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class BannerOneOfOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemBannerOneOfOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanSystemBannerData:
    login: Union[OneOfOptionsDef1, BannerOneOfOptionsDef2, OneOfOptionsDef3]
    motd: Union[OneOfOptionsDef1, SystemBannerOneOfOptionsDef2, OneOfOptionsDef3]


@dataclass
class BannerPayload:
    """
    Banner profile parcel schema for PUT request
    """

    data: SdwanSystemBannerData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanSystemBannerPayload:
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
    # Banner profile parcel schema for PUT request
    payload: Optional[BannerPayload] = _field(default=None)


@dataclass
class EditBannerProfileParcelForSystemPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanSystemBannerOneOfOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanSystemBannerOneOfOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanSystemBannerData:
    login: Union[OneOfOptionsDef1, SdwanSystemBannerOneOfOptionsDef2, OneOfOptionsDef3]
    motd: Union[OneOfOptionsDef1, FeatureProfileSdwanSystemBannerOneOfOptionsDef2, OneOfOptionsDef3]


@dataclass
class EditBannerProfileParcelForSystemPutRequest:
    """
    Banner profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanSystemBannerData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
