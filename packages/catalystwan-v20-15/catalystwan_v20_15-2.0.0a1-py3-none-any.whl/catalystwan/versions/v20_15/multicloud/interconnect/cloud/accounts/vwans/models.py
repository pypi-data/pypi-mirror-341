# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

CloudTypeParam = Literal["AWS", "AZURE", "GCP"]


@dataclass
class AzureVirtualWanTagList:
    """
    Azure Virtual WAN Tag Object
    """

    name: Optional[str] = _field(default=None)
    value: Optional[str] = _field(default=None)


@dataclass
class AzureVirtualWan:
    """
    Azure Virtual Wan
    """

    name: str
    region: str
    resource_group_name: str = _field(metadata={"alias": "resourceGroupName"})
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    # Cloud account name
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    allow_branch_to_branch_traffic: Optional[bool] = _field(
        default=None, metadata={"alias": "allowBranchToBranchTraffic"}
    )
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    description: Optional[str] = _field(default=None)
    id: Optional[str] = _field(default=None)
    provisioning_state: Optional[str] = _field(
        default=None, metadata={"alias": "provisioningState"}
    )
    tag_list: Optional[List[AzureVirtualWanTagList]] = _field(
        default=None, metadata={"alias": "tagList"}
    )
    virtual_wan_type: Optional[str] = _field(default=None, metadata={"alias": "virtualWanType"})
    vnet_tovnet_traffic_enabled: Optional[bool] = _field(
        default=None, metadata={"alias": "vnetTovnetTrafficEnabled"}
    )


@dataclass
class InlineResponse2009VWans:
    # Azure Virtual Wan
    v_wan: Optional[AzureVirtualWan] = _field(default=None, metadata={"alias": "vWan"})
    v_wan_in_use: Optional[bool] = _field(default=None, metadata={"alias": "vWanInUse"})


@dataclass
class InlineResponse2009:
    v_wans: Optional[List[InlineResponse2009VWans]] = _field(
        default=None, metadata={"alias": "vWans"}
    )
