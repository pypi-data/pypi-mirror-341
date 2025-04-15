# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

Mode = Literal["SDWANaaS", "default"]

Env = Literal["PRODUCTION", "PROD_STAGING", "STAGING"]


@dataclass
class InitBlobVmanageInitBlobInternalCredentials:
    password: str
    # Url to reset credentials
    reset_url: str = _field(metadata={"alias": "resetUrl"})
    user_name: str = _field(metadata={"alias": "userName"})


@dataclass
class InitBlobVmanageInitBlobJwtCredentials:
    # client id
    client_id: str
    # client secret
    client_secret: str
    # Url to reset credentials
    reset_url: str = _field(metadata={"alias": "resetUrl"})
    # Url to fetch token
    token_url: str = _field(metadata={"alias": "tokenUrl"})


@dataclass
class InitBlobVmanageInitBlobPnp:
    # client id
    client_id: str
    # client secret
    client_secret: str
    # Url to reset credentials
    reset_url: str = _field(metadata={"alias": "resetUrl"})
    # PnP environment
    env: Optional[Env] = _field(default=None)


@dataclass
class InitBlobVmanageInitBlob:
    internal_credentials: InitBlobVmanageInitBlobInternalCredentials = _field(
        metadata={"alias": "internalCredentials"}
    )
    jwt_credentials: InitBlobVmanageInitBlobJwtCredentials = _field(
        metadata={"alias": "jwtCredentials"}
    )
    # vManage Mode
    mode: Mode  # pytype: disable=annotation-type-mismatch
    pnp: InitBlobVmanageInitBlobPnp
    # SDWAN Portal Url
    sdwan_portal_url: Optional[str] = _field(default=None, metadata={"alias": "sdwanPortalUrl"})
    # Webhook Url to send notifications
    webhook_url: Optional[str] = _field(default=None, metadata={"alias": "webhookUrl"})


@dataclass
class InitBlob:
    vmanage_init_blob: Optional[InitBlobVmanageInitBlob] = _field(default=None)
