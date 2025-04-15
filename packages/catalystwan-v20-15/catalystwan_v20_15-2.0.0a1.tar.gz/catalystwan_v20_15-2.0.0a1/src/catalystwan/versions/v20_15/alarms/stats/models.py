# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Dict, Optional


@dataclass
class EventStats:
    discarded_events: Optional[int] = _field(default=None, metadata={"alias": "Discarded Events"})
    processed_events: Optional[int] = _field(default=None, metadata={"alias": "Processed Events"})
    total: Optional[int] = _field(default=None, metadata={"alias": "Total"})


@dataclass
class AlarmStatsResponseCorrelationEngine:
    added_events: Optional[int] = _field(default=None, metadata={"alias": "Added Events"})


@dataclass
class AlarmStatsResponse:
    correlation_db_manipulator: Optional[Dict[str, EventStats]] = _field(
        default=None, metadata={"alias": "Correlation DB Manipulator"}
    )
    correlation_engine: Optional[AlarmStatsResponseCorrelationEngine] = _field(
        default=None, metadata={"alias": "Correlation Engine"}
    )
    link_update_correlator: Optional[Dict[str, str]] = _field(
        default=None, metadata={"alias": "Link Update Correlator"}
    )
