# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DataUsage:
    """
    Data usage limit info .
    """

    usage_limit: Optional[int] = _field(default=None, metadata={"alias": "usageLimit"})
    usage_limit_unit: Optional[str] = _field(default=None, metadata={"alias": "usageLimitUnit"})
    use_default_rating: Optional[bool] = _field(
        default=None, metadata={"alias": "useDefaultRating"}
    )


@dataclass
class RatePlan:
    """
    List of rate plans.
    """

    # Name of the rate plan.
    name: str
    # Rate plan type.
    type_: str = _field(metadata={"alias": "type"})
    # Data usage limit info .
    data_usage: Optional[DataUsage] = _field(default=None, metadata={"alias": "dataUsage"})


@dataclass
class RatePlansResponse:
    # Indicator whether the payload is the last payload.
    last_page: bool = _field(metadata={"alias": "lastPage"})
    # Page Number.
    page_number: int = _field(metadata={"alias": "pageNumber"})
    # List of rate plans.
    rate_plans: List[RatePlan] = _field(metadata={"alias": "ratePlans"})
