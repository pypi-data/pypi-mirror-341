# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class Apn:
    """
    List of APNs associated with the Comm Plan
    """

    name: str


@dataclass
class LteApn:
    """
    List of LTE APNs associated with the Comm Plan.Empty if lteEnabled is false
    """

    name: str


@dataclass
class CommunicationPlan:
    # List of APNs associated with the Comm Plan
    apns: List[Apn]
    # List of LTE APNs associated with the Comm Plan.Empty if lteEnabled is false
    lte_apns: List[LteApn] = _field(metadata={"alias": "lteApns"})
    # Specifies whether the Comm Plan has LTE enabled
    lte_enabled: bool = _field(metadata={"alias": "lteEnabled"})
    # Name of the communication plan.
    name: str
    # Description of the communication plan.
    comm_plan_description: Optional[str] = _field(
        default=None, metadata={"alias": "commPlanDescription"}
    )
    comm_plan_name: Optional[str] = _field(default=None, metadata={"alias": "commPlanName"})


@dataclass
class CommunicationPlansResponse:
    # List of communication plans.
    communication_plans: List[CommunicationPlan] = _field(metadata={"alias": "communicationPlans"})
    # Page Number.
    page_number: int = _field(metadata={"alias": "pageNumber"})
    comm_plans: Optional[List[CommunicationPlan]] = _field(
        default=None, metadata={"alias": "commPlans"}
    )
