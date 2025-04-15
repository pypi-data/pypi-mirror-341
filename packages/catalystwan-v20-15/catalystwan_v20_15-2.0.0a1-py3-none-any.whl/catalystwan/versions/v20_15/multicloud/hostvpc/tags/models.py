# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class HostVpcTagResponse:
    account_id: str = _field(metadata={"alias": "accountId"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpc_id: str = _field(metadata={"alias": "hostVpcId"})
    region: str
    # Used for Azure and Azure GovCloud cloud types
    vnet_id: str = _field(metadata={"alias": "vnetId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpc_name: Optional[str] = _field(default=None, metadata={"alias": "hostVpcName"})
    # Used for Azure and Azure GovCloud cloud types
    resource_groups: Optional[str] = _field(default=None, metadata={"alias": "resourceGroups"})
    tag: Optional[str] = _field(default=None)
    # Used for Azure and Azure GovCloud cloud types
    vnet_key: Optional[str] = _field(default=None, metadata={"alias": "vnetKey"})
    # Used for Azure and Azure GovCloud cloud types
    vpc_name: Optional[str] = _field(default=None, metadata={"alias": "vpcName"})


@dataclass
class Taskid:
    """
    Task id for polling status
    """

    id: Optional[str] = _field(default=None)


@dataclass
class AllOfhostVpcTagPutHostVpcsItems:
    """
    Used for AWS, AWS GovCloud and GCP cloud types
    """

    account_id: str = _field(metadata={"alias": "accountId"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpc_id: str = _field(metadata={"alias": "hostVpcId"})
    region: str
    # Used for Azure and Azure GovCloud cloud types
    vnet_id: str = _field(metadata={"alias": "vnetId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    cgw_attachment: Optional[str] = _field(default=None, metadata={"alias": "cgwAttachment"})
    cgw_auto_attachment_flag: Optional[bool] = _field(
        default=None, metadata={"alias": "cgwAutoAttachmentFlag"}
    )
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpc_name: Optional[str] = _field(default=None, metadata={"alias": "hostVpcName"})
    id: Optional[str] = _field(default=None)
    interconnect_tag: Optional[str] = _field(default=None, metadata={"alias": "interconnectTag"})
    label: Optional[str] = _field(default=None)
    # Used for Azure and Azure GovCloud cloud types
    resource_groups: Optional[str] = _field(default=None, metadata={"alias": "resourceGroups"})
    tag: Optional[str] = _field(default=None)
    # Used for Azure and Azure GovCloud cloud types
    vnet_key: Optional[str] = _field(default=None, metadata={"alias": "vnetKey"})
    # Used for Azure and Azure GovCloud cloud types
    vpc_name: Optional[str] = _field(default=None, metadata={"alias": "vpcName"})


@dataclass
class AllOfhostVpcTagPutVnetsItems:
    """
    Used for Azure and Azure GovCloud cloud types
    """

    account_id: str = _field(metadata={"alias": "accountId"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpc_id: str = _field(metadata={"alias": "hostVpcId"})
    region: str
    # Used for Azure and Azure GovCloud cloud types
    vnet_id: str = _field(metadata={"alias": "vnetId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    cgw_attachment: Optional[str] = _field(default=None, metadata={"alias": "cgwAttachment"})
    cgw_auto_attachment_flag: Optional[bool] = _field(
        default=None, metadata={"alias": "cgwAutoAttachmentFlag"}
    )
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpc_name: Optional[str] = _field(default=None, metadata={"alias": "hostVpcName"})
    id: Optional[str] = _field(default=None)
    interconnect_tag: Optional[str] = _field(default=None, metadata={"alias": "interconnectTag"})
    label: Optional[str] = _field(default=None)
    # Used for Azure and Azure GovCloud cloud types
    resource_groups: Optional[str] = _field(default=None, metadata={"alias": "resourceGroups"})
    tag: Optional[str] = _field(default=None)
    # Used for Azure and Azure GovCloud cloud types
    vnet_key: Optional[str] = _field(default=None, metadata={"alias": "vnetKey"})
    # Used for Azure and Azure GovCloud cloud types
    vpc_name: Optional[str] = _field(default=None, metadata={"alias": "vpcName"})


@dataclass
class HostVpcTagPut:
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpcs: Optional[List[AllOfhostVpcTagPutHostVpcsItems]] = _field(
        default=None, metadata={"alias": "hostVpcs"}
    )
    interconnect_tag: Optional[bool] = _field(default=None, metadata={"alias": "interconnectTag"})
    tag_name: Optional[str] = _field(default=None, metadata={"alias": "tagName"})
    # Used for Azure and Azure GovCloud cloud types
    vnets: Optional[List[AllOfhostVpcTagPutVnetsItems]] = _field(default=None)


@dataclass
class AllOfhostVpcTagPostHostVpcsItems:
    """
    Used for AWS, AWS GovCloud and GCP cloud types
    """

    account_id: str = _field(metadata={"alias": "accountId"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpc_id: str = _field(metadata={"alias": "hostVpcId"})
    region: str
    # Used for Azure and Azure GovCloud cloud types
    vnet_id: str = _field(metadata={"alias": "vnetId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpc_name: Optional[str] = _field(default=None, metadata={"alias": "hostVpcName"})
    id: Optional[str] = _field(default=None)
    label: Optional[str] = _field(default=None)
    # Used for Azure and Azure GovCloud cloud types
    resource_groups: Optional[str] = _field(default=None, metadata={"alias": "resourceGroups"})
    # Used for Azure and Azure GovCloud cloud types
    vnet_key: Optional[str] = _field(default=None, metadata={"alias": "vnetKey"})
    # Used for Azure and Azure GovCloud cloud types
    vpc_name: Optional[str] = _field(default=None, metadata={"alias": "vpcName"})


@dataclass
class AllOfhostVpcTagPostVnetsItems:
    """
    Used for Azure and Azure GovCloud cloud types
    """

    account_id: str = _field(metadata={"alias": "accountId"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpc_id: str = _field(metadata={"alias": "hostVpcId"})
    region: str
    # Used for Azure and Azure GovCloud cloud types
    vnet_id: str = _field(metadata={"alias": "vnetId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    cgw_attachment: Optional[str] = _field(default=None, metadata={"alias": "cgwAttachment"})
    cgw_auto_attachment_flag: Optional[bool] = _field(
        default=None, metadata={"alias": "cgwAutoAttachmentFlag"}
    )
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpc_name: Optional[str] = _field(default=None, metadata={"alias": "hostVpcName"})
    id: Optional[str] = _field(default=None)
    label: Optional[str] = _field(default=None)
    # Used for Azure and Azure GovCloud cloud types
    resource_groups: Optional[str] = _field(default=None, metadata={"alias": "resourceGroups"})
    # Used for Azure and Azure GovCloud cloud types
    vnet_key: Optional[str] = _field(default=None, metadata={"alias": "vnetKey"})
    # Used for Azure and Azure GovCloud cloud types
    vpc_name: Optional[str] = _field(default=None, metadata={"alias": "vpcName"})


@dataclass
class HostVpcTagPost:
    # Used for AWS, AWS GovCloud and GCP cloud types
    host_vpcs: Optional[List[AllOfhostVpcTagPostHostVpcsItems]] = _field(
        default=None, metadata={"alias": "hostVpcs"}
    )
    interconnect_tag: Optional[bool] = _field(default=None, metadata={"alias": "interconnectTag"})
    tag_name: Optional[str] = _field(default=None, metadata={"alias": "tagName"})
    # Used for Azure and Azure GovCloud cloud types
    vnets: Optional[List[AllOfhostVpcTagPostVnetsItems]] = _field(default=None)
