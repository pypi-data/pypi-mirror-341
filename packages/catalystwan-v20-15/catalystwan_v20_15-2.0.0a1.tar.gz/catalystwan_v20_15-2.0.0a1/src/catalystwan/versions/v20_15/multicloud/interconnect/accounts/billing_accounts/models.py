# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class InterconnectBillingAccountInfo:
    """
    Interconnect billing account Information
    """

    # Interconnect billing account Id
    edge_billing_account_id: Optional[str] = _field(
        default=None, metadata={"alias": "edgeBillingAccountId"}
    )
    # Interconnect billing account name
    edge_billing_account_name: Optional[str] = _field(
        default=None, metadata={"alias": "edgeBillingAccountName"}
    )


@dataclass
class InlineResponse2001:
    edge_billing_account_info_list: Optional[List[InterconnectBillingAccountInfo]] = _field(
        default=None, metadata={"alias": "edgeBillingAccountInfoList"}
    )
