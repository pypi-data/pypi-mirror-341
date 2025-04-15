# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class SetLogLevelPostRequest:
    log_level: Optional[str] = _field(default=None, metadata={"alias": "logLevel"})
    logger_name: Optional[str] = _field(default=None, metadata={"alias": "loggerName"})
