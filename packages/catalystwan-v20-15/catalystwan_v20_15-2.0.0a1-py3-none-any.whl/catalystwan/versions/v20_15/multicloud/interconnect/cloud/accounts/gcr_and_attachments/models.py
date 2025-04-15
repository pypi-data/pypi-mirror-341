# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

CloudTypeParam = Literal["AWS", "AZURE", "GCP"]


@dataclass
class GcpInterconnectAttachment:
    """
    Google cloud Interconnect Attachment Object.
    """

    cloud_router_ip_address: Optional[str] = _field(
        default=None, metadata={"alias": "cloudRouterIpAddress"}
    )
    customer_ip_address: Optional[str] = _field(
        default=None, metadata={"alias": "customerIpAddress"}
    )
    id: Optional[str] = _field(default=None)
    # MTU of the Interconnect attachment
    mtu: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    pairing_key: Optional[str] = _field(default=None, metadata={"alias": "pairingKey"})
    region: Optional[str] = _field(default=None)
    # Option to create Interconnect attachment in secondary zone
    secondary_zone: Optional[str] = _field(default=None, metadata={"alias": "secondaryZone"})
    state: Optional[str] = _field(default=None)


@dataclass
class GcpCloudRouter:
    """
    Google cloud GCR Object.
    """

    name: str
    network: str
    # List of GCR Attachments
    attachment_details: Optional[List[GcpInterconnectAttachment]] = _field(
        default=None, metadata={"alias": "attachmentDetails"}
    )
    cloud_router_asn: Optional[str] = _field(default=None, metadata={"alias": "cloudRouterAsn"})
    id: Optional[str] = _field(default=None)
    region: Optional[str] = _field(default=None)


@dataclass
class InlineResponse20010:
    gcp_cloud_routers: Optional[List[GcpCloudRouter]] = _field(
        default=None, metadata={"alias": "gcpCloudRouters"}
    )
