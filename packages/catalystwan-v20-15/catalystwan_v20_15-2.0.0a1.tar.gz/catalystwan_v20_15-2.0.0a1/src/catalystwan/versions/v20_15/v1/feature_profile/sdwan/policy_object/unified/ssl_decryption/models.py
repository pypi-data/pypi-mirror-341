# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DecryptAndDropStringDef = Literal["decrypt", "drop"]

CertificateRevocationStatusDef = Literal["none", "ocsp"]

NoDecryptAndDropStringDef = Literal["drop", "no-decrypt"]

FailureModeDef = Literal["close", "open"]

KeyModulusDef = Literal["1024", "2048", "4096"]

EckeyTypeDef = Literal["P256", "P384", "P521"]

MinTlsVerDef = Literal["TLSv1", "TLSv1.1", "TLSv1.2"]

CaTpLabelDef = Literal["PROXY-SIGNING-CA"]


@dataclass
class CreateSecurityProfileParcelPostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class Data:
    ca_cert_bundle: Optional[Any] = _field(default=None, metadata={"alias": "caCertBundle"})


@dataclass
class CreateSecurityProfileParcelPostRequest1:
    data: Data
    # Will be auto generated
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfSslEnableOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfExpiredCertificateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUntrustedCertificateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCertificateRevocationStatusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CertificateRevocationStatusDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUnknownStatusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUnsupportedProtocolVersionsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NoDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUnsupportedCipherSuitesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NoDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfFailureModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FailureModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class DefaultDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfCaCertBundleOptionsDef1:
    default: DefaultDef


@dataclass
class FileNameDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class BundleStringDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfCaCertBundleOptionsDef2:
    bundle_string: BundleStringDef = _field(metadata={"alias": "bundleString"})
    default: DefaultDef
    file_name: FileNameDef = _field(metadata={"alias": "fileName"})


@dataclass
class OneOfKeyModulusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: KeyModulusDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEckeyTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EckeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCertificateLifetimeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfMinTlsVerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MinTlsVerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCaTpLabelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CaTpLabelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SslDecryptionData:
    ssl_enable: OneOfSslEnableOptionsDef = _field(metadata={"alias": "sslEnable"})
    ca_cert_bundle: Optional[Union[OneOfCaCertBundleOptionsDef1, OneOfCaCertBundleOptionsDef2]] = (
        _field(default=None, metadata={"alias": "caCertBundle"})
    )
    ca_tp_label: Optional[OneOfCaTpLabelOptionsDef] = _field(
        default=None, metadata={"alias": "caTpLabel"}
    )
    certificate_lifetime: Optional[OneOfCertificateLifetimeOptionsDef] = _field(
        default=None, metadata={"alias": "certificateLifetime"}
    )
    certificate_revocation_status: Optional[OneOfCertificateRevocationStatusOptionsDef] = _field(
        default=None, metadata={"alias": "certificateRevocationStatus"}
    )
    eckey_type: Optional[OneOfEckeyTypeOptionsDef] = _field(
        default=None, metadata={"alias": "eckeyType"}
    )
    expired_certificate: Optional[OneOfExpiredCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "expiredCertificate"}
    )
    failure_mode: Optional[OneOfFailureModeOptionsDef] = _field(
        default=None, metadata={"alias": "failureMode"}
    )
    key_modulus: Optional[OneOfKeyModulusOptionsDef] = _field(
        default=None, metadata={"alias": "keyModulus"}
    )
    min_tls_ver: Optional[OneOfMinTlsVerOptionsDef] = _field(
        default=None, metadata={"alias": "minTlsVer"}
    )
    unknown_status: Optional[OneOfUnknownStatusOptionsDef] = _field(
        default=None, metadata={"alias": "unknownStatus"}
    )
    unsupported_cipher_suites: Optional[OneOfUnsupportedCipherSuitesOptionsDef] = _field(
        default=None, metadata={"alias": "unsupportedCipherSuites"}
    )
    unsupported_protocol_versions: Optional[OneOfUnsupportedProtocolVersionsOptionsDef] = _field(
        default=None, metadata={"alias": "unsupportedProtocolVersions"}
    )
    untrusted_certificate: Optional[OneOfUntrustedCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "untrustedCertificate"}
    )


@dataclass
class CreateSecurityProfileParcelPostRequest2:
    data: SslDecryptionData
    # Will be auto generated
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload1:
    data: Data
    # Will be auto generated
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class UnifiedSslDecryptionData:
    ssl_enable: OneOfSslEnableOptionsDef = _field(metadata={"alias": "sslEnable"})
    ca_cert_bundle: Optional[Union[OneOfCaCertBundleOptionsDef1, OneOfCaCertBundleOptionsDef2]] = (
        _field(default=None, metadata={"alias": "caCertBundle"})
    )
    ca_tp_label: Optional[OneOfCaTpLabelOptionsDef] = _field(
        default=None, metadata={"alias": "caTpLabel"}
    )
    certificate_lifetime: Optional[OneOfCertificateLifetimeOptionsDef] = _field(
        default=None, metadata={"alias": "certificateLifetime"}
    )
    certificate_revocation_status: Optional[OneOfCertificateRevocationStatusOptionsDef] = _field(
        default=None, metadata={"alias": "certificateRevocationStatus"}
    )
    eckey_type: Optional[OneOfEckeyTypeOptionsDef] = _field(
        default=None, metadata={"alias": "eckeyType"}
    )
    expired_certificate: Optional[OneOfExpiredCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "expiredCertificate"}
    )
    failure_mode: Optional[OneOfFailureModeOptionsDef] = _field(
        default=None, metadata={"alias": "failureMode"}
    )
    key_modulus: Optional[OneOfKeyModulusOptionsDef] = _field(
        default=None, metadata={"alias": "keyModulus"}
    )
    min_tls_ver: Optional[OneOfMinTlsVerOptionsDef] = _field(
        default=None, metadata={"alias": "minTlsVer"}
    )
    unknown_status: Optional[OneOfUnknownStatusOptionsDef] = _field(
        default=None, metadata={"alias": "unknownStatus"}
    )
    unsupported_cipher_suites: Optional[OneOfUnsupportedCipherSuitesOptionsDef] = _field(
        default=None, metadata={"alias": "unsupportedCipherSuites"}
    )
    unsupported_protocol_versions: Optional[OneOfUnsupportedProtocolVersionsOptionsDef] = _field(
        default=None, metadata={"alias": "unsupportedProtocolVersions"}
    )
    untrusted_certificate: Optional[OneOfUntrustedCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "untrustedCertificate"}
    )


@dataclass
class Payload2:
    data: UnifiedSslDecryptionData
    # Will be auto generated
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
    # ssl-decryption profile parcel schema for POST request
    payload: Optional[Union[Payload1, Payload2]] = _field(default=None)
