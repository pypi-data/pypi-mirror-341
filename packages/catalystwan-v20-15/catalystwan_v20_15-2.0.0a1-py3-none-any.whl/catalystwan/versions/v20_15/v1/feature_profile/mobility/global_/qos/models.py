# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfGigInterfaceRateDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfGigInterfaceRateDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfGigInterfaceRateDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GigabitEthernet00QosConfig:
    """
    GigabitEthernet0/0 IEEE 802.3z interface QOS configuration
    """

    rate: Union[OneOfGigInterfaceRateDef1, OneOfGigInterfaceRateDef2, OneOfGigInterfaceRateDef3]


@dataclass
class OneOfCellularInterfaceRateDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfCellularInterfaceRateDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfCellularInterfaceRateDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Cellular1QosConfig:
    """
    Cellular1 interface QOS configuration
    """

    rate: Union[
        OneOfCellularInterfaceRateDef1,
        OneOfCellularInterfaceRateDef2,
        OneOfCellularInterfaceRateDef3,
    ]


@dataclass
class QosData:
    # Cellular1 interface QOS configuration
    cellular1_qos_config: Cellular1QosConfig = _field(metadata={"alias": "cellular1QosConfig"})
    enable_qos: Union[
        OneOfOnBooleanDefaultFalseOptionsDef1,
        OneOfOnBooleanDefaultFalseOptionsDef2,
        OneOfOnBooleanDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "enableQos"})
    # GigabitEthernet0/0 IEEE 802.3z interface QOS configuration
    gigabit_ethernet00_qos_config: GigabitEthernet00QosConfig = _field(
        metadata={"alias": "gigabitEthernet00QosConfig"}
    )


@dataclass
class Payload:
    """
    AON QOS profile parcel schema for post and put requests
    """

    data: QosData
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
    # AON QOS profile parcel schema for post and put requests
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListMobilityGlobalQosPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateQosFeatureForGlobalPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalQosData:
    # Cellular1 interface QOS configuration
    cellular1_qos_config: Cellular1QosConfig = _field(metadata={"alias": "cellular1QosConfig"})
    enable_qos: Union[
        OneOfOnBooleanDefaultFalseOptionsDef1,
        OneOfOnBooleanDefaultFalseOptionsDef2,
        OneOfOnBooleanDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "enableQos"})
    # GigabitEthernet0/0 IEEE 802.3z interface QOS configuration
    gigabit_ethernet00_qos_config: GigabitEthernet00QosConfig = _field(
        metadata={"alias": "gigabitEthernet00QosConfig"}
    )


@dataclass
class CreateQosFeatureForGlobalPostRequest:
    """
    AON QOS profile parcel schema for post and put requests
    """

    data: GlobalQosData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleMobilityGlobalQosPayload:
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
    # AON QOS profile parcel schema for post and put requests
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditQosFeatureForGlobalPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class MobilityGlobalQosData:
    # Cellular1 interface QOS configuration
    cellular1_qos_config: Cellular1QosConfig = _field(metadata={"alias": "cellular1QosConfig"})
    enable_qos: Union[
        OneOfOnBooleanDefaultFalseOptionsDef1,
        OneOfOnBooleanDefaultFalseOptionsDef2,
        OneOfOnBooleanDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "enableQos"})
    # GigabitEthernet0/0 IEEE 802.3z interface QOS configuration
    gigabit_ethernet00_qos_config: GigabitEthernet00QosConfig = _field(
        metadata={"alias": "gigabitEthernet00QosConfig"}
    )


@dataclass
class EditQosFeatureForGlobalPutRequest:
    """
    AON QOS profile parcel schema for post and put requests
    """

    data: MobilityGlobalQosData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
