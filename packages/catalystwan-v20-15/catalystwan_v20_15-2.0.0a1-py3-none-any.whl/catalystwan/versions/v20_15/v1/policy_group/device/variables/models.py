# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

Solution = Literal["sd-routing", "sdwan"]


@dataclass
class Variables:
    name: str
    value: Union[str, int, int, bool, List[None]]


@dataclass
class Devices:
    # Device unique id
    device_id: str = _field(metadata={"alias": "device-id"})
    # Variable object for the device
    variables: List[Variables]


@dataclass
class CreatePolicyGroupDeviceVariablesPutRequest:
    """
    Variables PUT request Schema
    """

    # Variables for devices
    devices: List[Devices]
    solution: Solution  # pytype: disable=annotation-type-mismatch


@dataclass
class VariablesVariables:
    # Name of the variable
    name: str
    # List of suggestions for the variable
    suggestions: Optional[List[str]] = _field(default=None)
    # Value of the variable
    value: Optional[str] = _field(default=None)


@dataclass
class VariablesDevices:
    # Unique identifier for the device
    device_id: str = _field(metadata={"alias": "device-id"})
    variables: List[VariablesVariables]


@dataclass
class Groups:
    # Variables associated with the group
    group_variables: List[Any] = _field(metadata={"alias": "group-variables"})
    # Name of the group
    name: str


@dataclass
class FetchPolicyGroupDeviceVariablesPostResponse:
    """
    Schema for the response of a GET request to retrieve config group variables
    """

    devices: List[VariablesDevices]
    # Family of the configuration
    family: str
    groups: List[Groups]


@dataclass
class FetchPolicyGroupDeviceVariablesPostRequest:
    """
    Variables POST request Schema
    """

    # ID of devices for which Variables need to be fetched
    device_ids: Optional[List[str]] = _field(default=None, metadata={"alias": "deviceIds"})
    # Variable object for the device
    suggestions: Optional[bool] = _field(default=None)
