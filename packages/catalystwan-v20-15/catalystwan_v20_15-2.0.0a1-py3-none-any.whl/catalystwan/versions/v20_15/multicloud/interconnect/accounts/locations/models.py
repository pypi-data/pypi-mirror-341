# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

EdgeType = Literal["EQUINIX", "MEGAPORT"]


@dataclass
class InterconnectLocationInfoMegaportMpMveInfo:
    image_name_list: Optional[List[str]] = _field(default=None, metadata={"alias": "imageNameList"})
    product_size_list: Optional[List[str]] = _field(
        default=None, metadata={"alias": "productSizeList"}
    )


@dataclass
class InterconnectLocationInfoAtt:
    att_ne_info: Optional[InterconnectLocationInfoMegaportMpMveInfo] = _field(
        default=None, metadata={"alias": "attNEInfo"}
    )
    metro_code: Optional[str] = _field(default=None, metadata={"alias": "metroCode"})
    metro_name: Optional[str] = _field(default=None, metadata={"alias": "metroName"})
    network_region: Optional[str] = _field(default=None, metadata={"alias": "networkRegion"})
    site_code: Optional[str] = _field(default=None, metadata={"alias": "siteCode"})
    status: Optional[str] = _field(default=None)


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
class InterconnectLocationInfoEquinix:
    eq_billing_account_info_list: Optional[List[InterconnectBillingAccountInfo]] = _field(
        default=None, metadata={"alias": "eqBillingAccountInfoList"}
    )
    eq_ne_info: Optional[InterconnectLocationInfoMegaportMpMveInfo] = _field(
        default=None, metadata={"alias": "eqNEInfo"}
    )
    metro_code: Optional[str] = _field(default=None, metadata={"alias": "metroCode"})
    metro_name: Optional[str] = _field(default=None, metadata={"alias": "metroName"})
    network_region: Optional[str] = _field(default=None, metadata={"alias": "networkRegion"})
    site_code: Optional[str] = _field(default=None, metadata={"alias": "siteCode"})
    status: Optional[str] = _field(default=None)


@dataclass
class InterconnectLocationInfoMegaport:
    address: Optional[str] = _field(default=None)
    country: Optional[str] = _field(default=None)
    live_date: Optional[str] = _field(default=None, metadata={"alias": "liveDate"})
    market: Optional[str] = _field(default=None)
    metro_name: Optional[str] = _field(default=None, metadata={"alias": "metroName"})
    mp_mve_info: Optional[InterconnectLocationInfoMegaportMpMveInfo] = _field(
        default=None, metadata={"alias": "mpMVEInfo"}
    )
    network_region: Optional[str] = _field(default=None, metadata={"alias": "networkRegion"})
    site_code: Optional[str] = _field(default=None, metadata={"alias": "siteCode"})
    status: Optional[str] = _field(default=None)


@dataclass
class InterconnectLocationsEdgeLocationInfoList:
    att_location_info: Optional[InterconnectLocationInfoAtt] = _field(
        default=None, metadata={"alias": "attLocationInfo"}
    )
    edge_type: Optional[EdgeType] = _field(default=None, metadata={"alias": "edgeType"})
    eq_location_info: Optional[InterconnectLocationInfoEquinix] = _field(
        default=None, metadata={"alias": "eqLocationInfo"}
    )
    location_id: Optional[str] = _field(default=None, metadata={"alias": "locationId"})
    location_name: Optional[str] = _field(default=None, metadata={"alias": "locationName"})
    mp_location_info: Optional[InterconnectLocationInfoMegaport] = _field(
        default=None, metadata={"alias": "mpLocationInfo"}
    )


@dataclass
class InterconnectLocations:
    edge_location_info_list: Optional[List[InterconnectLocationsEdgeLocationInfoList]] = _field(
        default=None, metadata={"alias": "edgeLocationInfoList"}
    )
