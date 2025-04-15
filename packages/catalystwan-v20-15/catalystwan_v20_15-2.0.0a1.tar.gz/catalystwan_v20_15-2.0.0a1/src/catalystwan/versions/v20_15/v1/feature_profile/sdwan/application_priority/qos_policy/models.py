# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]


@dataclass
class CreatePolicyApplicationProfileParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfTargetInterfacesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfTargetInterfacesOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Target:
    """
    Interfaces
    """

    interfaces: Union[OneOfTargetInterfacesOptionsDef1, OneOfTargetInterfacesOptionsDef2]


@dataclass
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ParcelReferenceDef:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfQosMapQosSchedulersDropsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfQosMapQosSchedulersQueueOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfQosMapQosSchedulersBandwidthPercentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfQosMapQosSchedulersSchedulingOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class QosSchedulers:
    bandwidth_percent: Optional[OneOfQosMapQosSchedulersBandwidthPercentOptionsDef] = _field(
        default=None, metadata={"alias": "bandwidthPercent"}
    )
    class_map_ref: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "classMapRef"}
    )
    drops: Optional[OneOfQosMapQosSchedulersDropsOptionsDef] = _field(default=None)
    queue: Optional[OneOfQosMapQosSchedulersQueueOptionsDef] = _field(default=None)
    scheduling: Optional[OneOfQosMapQosSchedulersSchedulingOptionsDef] = _field(default=None)


@dataclass
class QosMap:
    """
    qos-map
    """

    qos_schedulers: Optional[List[QosSchedulers]] = _field(
        default=None, metadata={"alias": "qosSchedulers"}
    )


@dataclass
class Data:
    # qos-map
    qos_map: Optional[QosMap] = _field(default=None, metadata={"alias": "qosMap"})
    # Interfaces
    target: Optional[Target] = _field(default=None)


@dataclass
class CreatePolicyApplicationProfileParcelPostRequest:
    """
    Policy qos profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class QosPolicyOneOfTargetInterfacesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class QosPolicyTarget:
    """
    Interfaces
    """

    interfaces: Union[QosPolicyOneOfTargetInterfacesOptionsDef1, OneOfTargetInterfacesOptionsDef2]


@dataclass
class QosPolicyOneOfQosMapQosSchedulersDropsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class QosPolicyOneOfQosMapQosSchedulersQueueOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class QosPolicyOneOfQosMapQosSchedulersBandwidthPercentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class QosPolicyOneOfQosMapQosSchedulersSchedulingOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class QosPolicyQosSchedulers:
    bandwidth_percent: Optional[QosPolicyOneOfQosMapQosSchedulersBandwidthPercentOptionsDef] = (
        _field(default=None, metadata={"alias": "bandwidthPercent"})
    )
    class_map_ref: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "classMapRef"}
    )
    drops: Optional[QosPolicyOneOfQosMapQosSchedulersDropsOptionsDef] = _field(default=None)
    queue: Optional[QosPolicyOneOfQosMapQosSchedulersQueueOptionsDef] = _field(default=None)
    scheduling: Optional[QosPolicyOneOfQosMapQosSchedulersSchedulingOptionsDef] = _field(
        default=None
    )


@dataclass
class QosPolicyQosMap:
    """
    qos-map
    """

    qos_schedulers: Optional[List[QosPolicyQosSchedulers]] = _field(
        default=None, metadata={"alias": "qosSchedulers"}
    )


@dataclass
class QosPolicyData:
    # qos-map
    qos_map: Optional[QosPolicyQosMap] = _field(default=None, metadata={"alias": "qosMap"})
    # Interfaces
    target: Optional[QosPolicyTarget] = _field(default=None)


@dataclass
class Payload:
    """
    Policy qos profile parcel schema for PUT request
    """

    data: QosPolicyData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanApplicationPriorityQosPolicyPayload:
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
    # Policy qos profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditPolicyApplicationProfileParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ApplicationPriorityQosPolicyOneOfTargetInterfacesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ApplicationPriorityQosPolicyTarget:
    """
    Interfaces
    """

    interfaces: Union[
        ApplicationPriorityQosPolicyOneOfTargetInterfacesOptionsDef1,
        OneOfTargetInterfacesOptionsDef2,
    ]


@dataclass
class ApplicationPriorityQosPolicyOneOfQosMapQosSchedulersDropsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ApplicationPriorityQosPolicyOneOfQosMapQosSchedulersQueueOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ApplicationPriorityQosPolicyOneOfQosMapQosSchedulersBandwidthPercentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ApplicationPriorityQosPolicyOneOfQosMapQosSchedulersSchedulingOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ApplicationPriorityQosPolicyQosSchedulers:
    bandwidth_percent: Optional[
        ApplicationPriorityQosPolicyOneOfQosMapQosSchedulersBandwidthPercentOptionsDef
    ] = _field(default=None, metadata={"alias": "bandwidthPercent"})
    class_map_ref: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "classMapRef"}
    )
    drops: Optional[ApplicationPriorityQosPolicyOneOfQosMapQosSchedulersDropsOptionsDef] = _field(
        default=None
    )
    queue: Optional[ApplicationPriorityQosPolicyOneOfQosMapQosSchedulersQueueOptionsDef] = _field(
        default=None
    )
    scheduling: Optional[
        ApplicationPriorityQosPolicyOneOfQosMapQosSchedulersSchedulingOptionsDef
    ] = _field(default=None)


@dataclass
class ApplicationPriorityQosPolicyQosMap:
    """
    qos-map
    """

    qos_schedulers: Optional[List[ApplicationPriorityQosPolicyQosSchedulers]] = _field(
        default=None, metadata={"alias": "qosSchedulers"}
    )


@dataclass
class ApplicationPriorityQosPolicyData:
    # qos-map
    qos_map: Optional[ApplicationPriorityQosPolicyQosMap] = _field(
        default=None, metadata={"alias": "qosMap"}
    )
    # Interfaces
    target: Optional[ApplicationPriorityQosPolicyTarget] = _field(default=None)


@dataclass
class EditPolicyApplicationProfileParcelPutRequest:
    """
    Policy qos profile parcel schema for PUT request
    """

    data: ApplicationPriorityQosPolicyData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
