# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Dict, List, Literal, Optional

ImageType = Literal[
    "ImageType{type='ackfile'}",
    "ImageType{type='container'}",
    "ImageType{type='dockertype'}",
    "ImageType{type='firmware'}",
    "ImageType{type='licensefile'}",
    "ImageType{type='lxc'}",
    "ImageType{type='na'}",
    "ImageType{type='rumreport'}",
    "ImageType{type='software'}",
    "ImageType{type='utdsignature'}",
    "ImageType{type='utdsignaturecustom'}",
    "ImageType{type='utdsignatureips'}",
    "ImageType{type='virtualmachine'}",
    "ImageType{type='virtualmachine-diskimg'}",
    "ImageType{type='virtualmachine-scaffold'}",
    "ImageType{type='waas'}",
]

UtdsignatureParam = Literal["utdsignature"]


@dataclass
class ImageData:
    application_vendor: Optional[str] = _field(
        default=None, metadata={"alias": "applicationVendor"}
    )
    application_vendor_vendor: Optional[str] = _field(
        default=None, metadata={"alias": "applicationVendorVendor"}
    )
    arch: Optional[str] = _field(default=None)
    controller_version: Optional[str] = _field(
        default=None, metadata={"alias": "controllerVersion"}
    )
    cw_version: Optional[str] = _field(default=None, metadata={"alias": "cwVersion"})
    description: Optional[str] = _field(default=None)
    display_checksum: Optional[str] = _field(default=None, metadata={"alias": "displayChecksum"})
    display_checksum_type: Optional[str] = _field(
        default=None, metadata={"alias": "displayChecksumType"}
    )
    display_checksum_validity: Optional[str] = _field(
        default=None, metadata={"alias": "displayChecksumValidity"}
    )
    family: Optional[str] = _field(default=None)
    file_entries: Optional[Dict[str, str]] = _field(default=None, metadata={"alias": "fileEntries"})
    file_name: Optional[str] = _field(default=None, metadata={"alias": "fileName"})
    file_size_str: Optional[str] = _field(default=None, metadata={"alias": "fileSizeStr"})
    file_sizebyte: Optional[str] = _field(default=None, metadata={"alias": "fileSizebyte"})
    image_properties_json: Optional[str] = _field(
        default=None, metadata={"alias": "imagePropertiesJson"}
    )
    image_type: Optional[ImageType] = _field(default=None, metadata={"alias": "imageType"})
    image_type_name: Optional[str] = _field(default=None, metadata={"alias": "imageTypeName"})
    md5_checksum: Optional[str] = _field(default=None, metadata={"alias": "md5Checksum"})
    network_function_type: Optional[str] = _field(
        default=None, metadata={"alias": "networkFunctionType"}
    )
    remote_server_id: Optional[str] = _field(default=None, metadata={"alias": "remoteServerId"})
    remote_servers: Optional[str] = _field(default=None, metadata={"alias": "remoteServers"})
    sha256_checksum: Optional[str] = _field(default=None, metadata={"alias": "sha256Checksum"})
    sha512_checksum: Optional[str] = _field(default=None, metadata={"alias": "sha512Checksum"})
    smu_compatible_with: Optional[str] = _field(
        default=None, metadata={"alias": "smuCompatibleWith"}
    )
    smu_defect_id: Optional[str] = _field(default=None, metadata={"alias": "smuDefectId"})
    smu_description: Optional[str] = _field(default=None, metadata={"alias": "smuDescription"})
    smu_type: Optional[str] = _field(default=None, metadata={"alias": "smuType"})
    storage_data: Optional[str] = _field(default=None, metadata={"alias": "storageData"})
    system_properties_xml: Optional[str] = _field(
        default=None, metadata={"alias": "systemPropertiesXml"}
    )
    tags: Optional[List[str]] = _field(default=None)
    temp_image_path: Optional[str] = _field(default=None, metadata={"alias": "tempImagePath"})
    updated_file_name: Optional[str] = _field(default=None, metadata={"alias": "updatedFileName"})
    version: Optional[str] = _field(default=None)
    version_type_name: Optional[str] = _field(default=None, metadata={"alias": "versionTypeName"})
    vnf_properties_json: Optional[str] = _field(
        default=None, metadata={"alias": "vnfPropertiesJson"}
    )
