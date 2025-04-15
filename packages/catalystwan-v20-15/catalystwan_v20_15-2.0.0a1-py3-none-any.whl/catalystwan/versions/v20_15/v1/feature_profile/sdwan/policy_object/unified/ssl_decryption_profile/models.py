# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

GlobalOptionTypeDef = Literal["global"]

CategoriesDef = Literal[
    "abortion",
    "abused-drugs",
    "adult-and-pornography",
    "alcohol-and-tobacco",
    "auctions",
    "bot-nets",
    "business-and-economy",
    "cdns",
    "cheating",
    "computer-and-internet-info",
    "computer-and-internet-security",
    "confirmed-spam-sources",
    "cult-and-occult",
    "dating",
    "dead-sites",
    "dynamic-content",
    "educational-institutions",
    "entertainment-and-arts",
    "fashion-and-beauty",
    "financial-services",
    "gambling",
    "games",
    "government",
    "gross",
    "hacking",
    "hate-and-racism",
    "health-and-medicine",
    "home",
    "hunting-and-fishing",
    "illegal",
    "image-and-video-search",
    "individual-stock-advice-and-tools",
    "internet-communications",
    "internet-portals",
    "job-search",
    "keyloggers-and-monitoring",
    "kids",
    "legal",
    "local-information",
    "malware-sites",
    "marijuana",
    "military",
    "motor-vehicles",
    "music",
    "news-and-media",
    "nudity",
    "online-greeting-cards",
    "online-personal-storage",
    "open-http-proxies",
    "p2p",
    "parked-sites",
    "pay-to-surf",
    "personal-sites-and-blogs",
    "philosophy-and-political-advocacy",
    "phishing-and-other-frauds",
    "private-ip-addresses",
    "proxy-avoid-and-anonymizers",
    "questionable",
    "real-estate",
    "recreation-and-hobbies",
    "reference-and-research",
    "religion",
    "search-engines",
    "sex-education",
    "shareware-and-freeware",
    "shopping",
    "social-network",
    "society",
    "spam-urls",
    "sports",
    "spyware-and-adware",
    "streaming-media",
    "swimsuits-and-intimate-apparel",
    "training-and-tools",
    "translation",
    "travel",
    "uncategorized",
    "unconfirmed-spam-sources",
    "violence",
    "weapons",
    "web-advertisements",
    "web-based-email",
    "web-hosting",
]

ThresholdDef = Literal["high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"]


@dataclass
class CreateSecurityProfileParcelPostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class OneOfDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeverDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSkipDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfReputationOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDecryptThresholdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ThresholdDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSkipDecryptThresholdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ThresholdDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfFailDecryptOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class RefIdOptionDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UrlAllowedList:
    ref_id: Optional[RefIdOptionDef] = _field(default=None, metadata={"alias": "refId"})


@dataclass
class UrlBlockedList:
    ref_id: Optional[RefIdOptionDef] = _field(default=None, metadata={"alias": "refId"})


@dataclass
class Data:
    decrypt_categories: OneOfDecryptCategoriesOptionsDef = _field(
        metadata={"alias": "decryptCategories"}
    )
    fail_decrypt: OneOfFailDecryptOptionsDef = _field(metadata={"alias": "failDecrypt"})
    never_decrypt_categories: OneOfNeverDecryptCategoriesOptionsDef = _field(
        metadata={"alias": "neverDecryptCategories"}
    )
    reputation: OneOfReputationOptionsDef
    decrypt_threshold: Optional[OneOfDecryptThresholdOptionsDef] = _field(
        default=None, metadata={"alias": "decryptThreshold"}
    )
    skip_decrypt_categories: Optional[OneOfSkipDecryptCategoriesOptionsDef] = _field(
        default=None, metadata={"alias": "skipDecryptCategories"}
    )
    skip_decrypt_threshold: Optional[OneOfSkipDecryptThresholdOptionsDef] = _field(
        default=None, metadata={"alias": "skipDecryptThreshold"}
    )
    url_allowed_list: Optional[UrlAllowedList] = _field(
        default=None, metadata={"alias": "urlAllowedList"}
    )
    url_blocked_list: Optional[UrlBlockedList] = _field(
        default=None, metadata={"alias": "urlBlockedList"}
    )


@dataclass
class CreateSecurityProfileParcelPostRequest:
    """
    ssl-decryption-profile profile parcel schema for POST request
    """

    data: Data
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload:
    """
    ssl-decryption-profile profile parcel schema for POST request
    """

    data: Data
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSecurityProfileParcelGetResponse:
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # ssl-decryption-profile profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)
