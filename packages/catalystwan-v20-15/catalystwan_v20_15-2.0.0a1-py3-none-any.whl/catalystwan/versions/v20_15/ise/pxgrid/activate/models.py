# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class ActivateResponse:
    """
    Response from PxGrid node activation on ISE, account PENDING on activated ENABLED after approve
    """

    account_state: Optional[str] = _field(default=None, metadata={"alias": "accountState"})
    version: Optional[str] = _field(default=None)


@dataclass
class ActivateBody:
    """
    Body for PxGrid node activate on ISE
    """

    description: Optional[str] = _field(default=None)
    px_grid_password: Optional[str] = _field(default=None, metadata={"alias": "pxGridPassword"})
    px_grid_user_name: Optional[str] = _field(default=None, metadata={"alias": "pxGridUserName"})
