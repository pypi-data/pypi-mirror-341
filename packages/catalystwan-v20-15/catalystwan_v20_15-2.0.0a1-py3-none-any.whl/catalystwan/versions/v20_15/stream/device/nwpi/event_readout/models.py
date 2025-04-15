# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class EventReadoutResponsePayloadInner:
    """
    Event Readout schema for GET response
    """

    application: Optional[str] = _field(default=None)
    drop_send_pkts: Optional[List[Any]] = _field(default=None, metadata={"alias": "dropSendPkts"})
    entry_time: Optional[int] = _field(default=None)
    event_hop_policy_info: Optional[List[Any]] = _field(
        default=None, metadata={"alias": "eventHopPolicyInfo"}
    )
    event_hop_statistics: Optional[List[Any]] = _field(
        default=None, metadata={"alias": "eventHopStatistics"}
    )
    event_hop_time_info: Optional[List[Any]] = _field(
        default=None, metadata={"alias": "eventHopTimeInfo"}
    )
    event_impacted_flow_num: Optional[List[Any]] = _field(
        default=None, metadata={"alias": "eventImpactedFlowNum"}
    )
    event_list: Optional[List[Any]] = _field(default=None, metadata={"alias": "eventList"})
    event_num: Optional[List[Any]] = _field(default=None, metadata={"alias": "eventNum"})
    readout_agg_flag: Optional[bool] = _field(default=None, metadata={"alias": "readoutAggFlag"})
    total_flow_num: Optional[int] = _field(default=None, metadata={"alias": "totalFlowNum"})
    trace_id: Optional[int] = _field(default=None)
