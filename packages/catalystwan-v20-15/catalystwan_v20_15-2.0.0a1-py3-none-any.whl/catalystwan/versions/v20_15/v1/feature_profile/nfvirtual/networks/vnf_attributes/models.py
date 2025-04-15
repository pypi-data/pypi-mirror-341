# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]


@dataclass
class CreateNfvirtualVnfAttributesParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNameOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSrcOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfChecksumOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUsernameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPasswordOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVersionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVnfTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfLowLatencyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSriovSupportedOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNocloudOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfThickDiskProvisioningOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfBootstrapCloudInitDriveTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRootImageDiskFormatOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfConsoleTypeSerialOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfVendorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Data:
    image_name: Union[OneOfNameOptionsDef1, OneOfNameOptionsDef2]
    src: OneOfSrcOptionsDef
    bootstrap_cloud_init_drive_type: Optional[OneOfBootstrapCloudInitDriveTypeOptionsDef] = _field(
        default=None
    )
    checksum: Optional[OneOfChecksumOptionsDef] = _field(default=None)
    console_type_serial: Optional[OneOfConsoleTypeSerialOptionsDef] = _field(default=None)
    low_latency: Optional[OneOfLowLatencyOptionsDef] = _field(default=None)
    nocloud: Optional[OneOfNocloudOptionsDef] = _field(default=None)
    password: Optional[OneOfPasswordOptionsDef] = _field(default=None)
    root_image_disk_format: Optional[OneOfRootImageDiskFormatOptionsDef] = _field(default=None)
    sriov_supported: Optional[OneOfSriovSupportedOptionsDef] = _field(default=None)
    thick_disk_provisioning: Optional[OneOfThickDiskProvisioningOptionsDef] = _field(default=None)
    username: Optional[OneOfUsernameOptionsDef] = _field(default=None)
    vendor: Optional[OneOfVendorOptionsDef] = _field(default=None)
    version: Optional[OneOfVersionOptionsDef] = _field(default=None)
    vnf_type: Optional[OneOfVnfTypeOptionsDef] = _field(default=None)


@dataclass
class CreateNfvirtualVnfAttributesParcelPostRequest:
    """
    VNF Attributes profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class VnfAttributesOneOfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesOneOfSrcOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesOneOfChecksumOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesOneOfUsernameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesOneOfPasswordOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesOneOfVersionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesOneOfVnfTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesOneOfBootstrapCloudInitDriveTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesOneOfRootImageDiskFormatOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesOneOfConsoleTypeSerialOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class VnfAttributesOneOfVendorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesData:
    image_name: Union[VnfAttributesOneOfNameOptionsDef1, OneOfNameOptionsDef2]
    src: VnfAttributesOneOfSrcOptionsDef
    bootstrap_cloud_init_drive_type: Optional[
        VnfAttributesOneOfBootstrapCloudInitDriveTypeOptionsDef
    ] = _field(default=None)
    checksum: Optional[VnfAttributesOneOfChecksumOptionsDef] = _field(default=None)
    console_type_serial: Optional[VnfAttributesOneOfConsoleTypeSerialOptionsDef] = _field(
        default=None
    )
    low_latency: Optional[OneOfLowLatencyOptionsDef] = _field(default=None)
    nocloud: Optional[OneOfNocloudOptionsDef] = _field(default=None)
    password: Optional[VnfAttributesOneOfPasswordOptionsDef] = _field(default=None)
    root_image_disk_format: Optional[VnfAttributesOneOfRootImageDiskFormatOptionsDef] = _field(
        default=None
    )
    sriov_supported: Optional[OneOfSriovSupportedOptionsDef] = _field(default=None)
    thick_disk_provisioning: Optional[OneOfThickDiskProvisioningOptionsDef] = _field(default=None)
    username: Optional[VnfAttributesOneOfUsernameOptionsDef] = _field(default=None)
    vendor: Optional[VnfAttributesOneOfVendorOptionsDef] = _field(default=None)
    version: Optional[VnfAttributesOneOfVersionOptionsDef] = _field(default=None)
    vnf_type: Optional[VnfAttributesOneOfVnfTypeOptionsDef] = _field(default=None)


@dataclass
class Payload:
    """
    VNF Attributes profile parcel schema for PUT request
    """

    data: VnfAttributesData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualNetworksVnfAttributesPayload:
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
    # VNF Attributes profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditNfvirtualVnfAttributesParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class NetworksVnfAttributesOneOfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksVnfAttributesOneOfSrcOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksVnfAttributesOneOfChecksumOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksVnfAttributesOneOfUsernameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksVnfAttributesOneOfPasswordOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksVnfAttributesOneOfVersionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksVnfAttributesOneOfVnfTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksVnfAttributesOneOfBootstrapCloudInitDriveTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksVnfAttributesOneOfRootImageDiskFormatOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksVnfAttributesOneOfConsoleTypeSerialOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class NetworksVnfAttributesOneOfVendorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksVnfAttributesData:
    image_name: Union[NetworksVnfAttributesOneOfNameOptionsDef1, OneOfNameOptionsDef2]
    src: NetworksVnfAttributesOneOfSrcOptionsDef
    bootstrap_cloud_init_drive_type: Optional[
        NetworksVnfAttributesOneOfBootstrapCloudInitDriveTypeOptionsDef
    ] = _field(default=None)
    checksum: Optional[NetworksVnfAttributesOneOfChecksumOptionsDef] = _field(default=None)
    console_type_serial: Optional[NetworksVnfAttributesOneOfConsoleTypeSerialOptionsDef] = _field(
        default=None
    )
    low_latency: Optional[OneOfLowLatencyOptionsDef] = _field(default=None)
    nocloud: Optional[OneOfNocloudOptionsDef] = _field(default=None)
    password: Optional[NetworksVnfAttributesOneOfPasswordOptionsDef] = _field(default=None)
    root_image_disk_format: Optional[NetworksVnfAttributesOneOfRootImageDiskFormatOptionsDef] = (
        _field(default=None)
    )
    sriov_supported: Optional[OneOfSriovSupportedOptionsDef] = _field(default=None)
    thick_disk_provisioning: Optional[OneOfThickDiskProvisioningOptionsDef] = _field(default=None)
    username: Optional[NetworksVnfAttributesOneOfUsernameOptionsDef] = _field(default=None)
    vendor: Optional[NetworksVnfAttributesOneOfVendorOptionsDef] = _field(default=None)
    version: Optional[NetworksVnfAttributesOneOfVersionOptionsDef] = _field(default=None)
    vnf_type: Optional[NetworksVnfAttributesOneOfVnfTypeOptionsDef] = _field(default=None)


@dataclass
class EditNfvirtualVnfAttributesParcelPutRequest:
    """
    VNF Attributes profile parcel schema for PUT request
    """

    data: NetworksVnfAttributesData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
