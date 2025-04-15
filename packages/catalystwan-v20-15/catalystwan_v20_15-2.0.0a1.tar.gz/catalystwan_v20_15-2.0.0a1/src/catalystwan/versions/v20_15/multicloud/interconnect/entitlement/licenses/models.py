# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class InterconnectLicense:
    current_status: Optional[str] = _field(default=None, metadata={"alias": "currentStatus"})
    edge_account_name: Optional[str] = _field(default=None, metadata={"alias": "edgeAccountName"})
    end_date: Optional[str] = _field(default=None, metadata={"alias": "endDate"})
    prod_type: Optional[str] = _field(default=None, metadata={"alias": "prodType"})
    sku: Optional[str] = _field(default=None)
    sku_days_for_expiry: Optional[int] = _field(
        default=None, metadata={"alias": "skuDaysForExpiry"}
    )
    sku_id: Optional[str] = _field(default=None, metadata={"alias": "skuId"})
    smart_account_id: Optional[str] = _field(default=None, metadata={"alias": "smartAccountId"})
    start_date: Optional[str] = _field(default=None, metadata={"alias": "startDate"})
    subscription_reference_id: Optional[str] = _field(
        default=None, metadata={"alias": "subscriptionReferenceId"}
    )
    technical_service_uid: Optional[str] = _field(
        default=None, metadata={"alias": "technicalServiceUid"}
    )
    virtual_account_id: Optional[str] = _field(default=None, metadata={"alias": "virtualAccountId"})
    vxc_bandwidth: Optional[str] = _field(default=None, metadata={"alias": "vxcBandwidth"})
    web_order_id: Optional[str] = _field(default=None, metadata={"alias": "webOrderId"})
