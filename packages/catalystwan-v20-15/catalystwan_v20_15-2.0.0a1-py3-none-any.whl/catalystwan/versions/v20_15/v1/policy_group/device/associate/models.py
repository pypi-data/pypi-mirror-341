# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from typing import List


@dataclass
class DeviceIdDef:
    id: str


@dataclass
class UpdatePolicyGroupAssociationPutRequest:
    """
    Policy Group Associate Put Request schema
    """

    # list of device ids that policy group need to be associated with
    devices: List[DeviceIdDef]


@dataclass
class AssociateDeviceIdDef:
    id: str


@dataclass
class CreatePolicyGroupAssociationPostRequest:
    """
    Policy Group Associate Post Request schema
    """

    # list of device ids that policy group need to be associated with
    devices: List[AssociateDeviceIdDef]


@dataclass
class DeviceAssociateDeviceIdDef:
    id: str


@dataclass
class DeletePolicyGroupAssociationDeleteRequest:
    """
    Policy Group Associate Delete Request schema
    """

    # list of device ids that policy group need to be associated with
    devices: List[DeviceAssociateDeviceIdDef]
