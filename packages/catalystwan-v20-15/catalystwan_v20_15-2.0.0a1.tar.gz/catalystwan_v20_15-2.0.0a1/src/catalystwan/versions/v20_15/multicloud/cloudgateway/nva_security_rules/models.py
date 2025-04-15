# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NvaRulesListRequestSecurityRulesList:
    destination_port_range: str = _field(metadata={"alias": "destinationPortRange"})
    protocol: str
    source_address_prefix: str = _field(metadata={"alias": "sourceAddressPrefix"})


@dataclass
class NvaRulesListRequest:
    security_rules_list: Optional[List[NvaRulesListRequestSecurityRulesList]] = _field(
        default=None, metadata={"alias": "securityRulesList"}
    )


@dataclass
class NvaRulesResponse:
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    expiration_time: Optional[str] = _field(default=None, metadata={"alias": "expirationTime"})
    nva_id: Optional[str] = _field(default=None, metadata={"alias": "nvaId"})
    resource_group_name: Optional[str] = _field(
        default=None, metadata={"alias": "resourceGroupName"}
    )
    rule_name: Optional[str] = _field(default=None, metadata={"alias": "ruleName"})
    security_rules_list: Optional[NvaRulesListRequest] = _field(
        default=None, metadata={"alias": "securityRulesList"}
    )


@dataclass
class Taskid:
    """
    Task id for polling status
    """

    id: Optional[str] = _field(default=None)
