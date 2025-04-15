# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class GetImagePropertiesImagePropertiesJsonImageProperties:
    application_description: Optional[str] = _field(
        default=None, metadata={"alias": "applicationDescription"}
    )
    application_max_instances: Optional[int] = _field(
        default=None, metadata={"alias": "applicationMaxInstances"}
    )
    application_vendor: Optional[str] = _field(
        default=None, metadata={"alias": "applicationVendor"}
    )
    arch: Optional[str] = _field(default=None)
    image_type: Optional[str] = _field(default=None, metadata={"alias": "imageType"})
    name: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)
    vnf_type: Optional[str] = _field(default=None)


@dataclass
class GetImagePropertiesImagePropertiesJson:
    image_properties: Optional[GetImagePropertiesImagePropertiesJsonImageProperties] = _field(
        default=None
    )


@dataclass
class GetImagePropertiesData:
    image_properties_json: Optional[GetImagePropertiesImagePropertiesJson] = _field(
        default=None, metadata={"alias": "imagePropertiesJson"}
    )


@dataclass
class GetImageProperties:
    data: Optional[List[GetImagePropertiesData]] = _field(default=None)
