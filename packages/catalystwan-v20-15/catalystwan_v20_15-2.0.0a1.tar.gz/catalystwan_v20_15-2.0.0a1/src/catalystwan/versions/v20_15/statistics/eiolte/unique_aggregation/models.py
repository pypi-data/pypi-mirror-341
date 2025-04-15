# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

Order = Literal["asc", "desc"]

OrderType = Literal["count", "key"]

Type = Literal["day", "hour", "minute", "month", "quater", "second", "week", "year"]

UniqueAggregationType = Literal[
    "argMax", "avg", "cardinality", "count", "max", "min", "sum", "top_hits"
]

Condition = Literal["AND", "OR"]

Operator = Literal[
    "between",
    "equal",
    "greater",
    "greater_or_equal",
    "hasAny",
    "in",
    "last_n_days",
    "last_n_hours",
    "last_n_weeks",
    "less",
    "less_or_equal",
    "not_equal",
    "not_in",
    "starts_with",
]

EiolteUniqueAggregationType = Literal[
    "array", "boolean", "date", "double", "int", "long", "number", "specialString", "string"
]

StatisticsEiolteUniqueAggregationType = Literal[
    "array", "boolean", "date", "double", "int", "long", "number", "specialString", "string"
]

Type1 = Literal[
    "array", "boolean", "date", "double", "int", "long", "number", "specialString", "string"
]


@dataclass
class DbQueryAggregationFieldObject:
    property: Any
    size: int
    order: Optional[Order] = _field(default=None)
    order_type: Optional[OrderType] = _field(default=None, metadata={"alias": "orderType"})
    sequence: Optional[int] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class DbQueryAggregationHistogramObject:
    order: Order  # pytype: disable=annotation-type-mismatch
    property: Any
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    interval: Optional[int] = _field(default=None)
    mindoccount: Optional[int] = _field(default=None)


@dataclass
class DbQueryAggregationMetricObject:
    property: Any
    type_: UniqueAggregationType = _field(
        metadata={"alias": "type"}
    )  # pytype: disable=annotation-type-mismatch
    order: Optional[str] = _field(default=None)
    sequence: Optional[str] = _field(default=None)
    size: Optional[str] = _field(default=None)


@dataclass
class DbQueryAggregationObject:
    field: Optional[List[DbQueryAggregationFieldObject]] = _field(default=None)
    histogram: Optional[DbQueryAggregationHistogramObject] = _field(default=None)
    metrics: Optional[List[DbQueryAggregationMetricObject]] = _field(default=None)


@dataclass
class DbQueryRuleObject:
    condition: Optional[Condition] = _field(default=None)
    field: Optional[Any] = _field(default=None)
    operator: Optional[Operator] = _field(default=None)
    rules: Optional[List["DbQueryRuleObject"]] = _field(default=None)
    type_: Optional[EiolteUniqueAggregationType] = _field(default=None, metadata={"alias": "type"})
    value: Optional[List[str]] = _field(default=None)


@dataclass
class DbQuerySpecObject:
    rules: List[DbQueryRuleObject]
    condition: Optional[Condition] = _field(default=None)
    field: Optional[Any] = _field(default=None)
    operator: Optional[Operator] = _field(default=None)
    type_: Optional[StatisticsEiolteUniqueAggregationType] = _field(
        default=None, metadata={"alias": "type"}
    )
    value: Optional[List[str]] = _field(default=None)


@dataclass
class DbQuerySortObject:
    field: Any
    order: Order  # pytype: disable=annotation-type-mismatch
    type_: Optional[Type1] = _field(default=None, metadata={"alias": "type"})


@dataclass
class StatisticsDbQueryParam:
    """
    Statistics search DB Query JSON object
    """

    aggregation: Optional[DbQueryAggregationObject] = _field(default=None)
    category: Optional[str] = _field(default=None)
    fields: Optional[List[Any]] = _field(default=None)
    plot_data: Optional[List[str]] = _field(default=None)
    query: Optional[DbQuerySpecObject] = _field(default=None)
    size: Optional[int] = _field(default=None)
    sort: Optional[List[DbQuerySortObject]] = _field(default=None)
