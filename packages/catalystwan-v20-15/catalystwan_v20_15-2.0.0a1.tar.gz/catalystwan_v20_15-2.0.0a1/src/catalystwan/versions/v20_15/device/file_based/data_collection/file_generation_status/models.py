# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class HandleFileGenerationStatusNotificationRequest:
    # Success or Failure reason in detail
    detailed_message: str = _field(metadata={"alias": "detailedMessage"})
    status: str
    # Transaction Id sent in the file generation RPC
    transaction_id: str = _field(metadata={"alias": "transactionId"})
    # MD5 checksum value of the file
    checksum: Optional[str] = _field(default=None)
    # Full path of the generated file
    file_name: Optional[str] = _field(default=None, metadata={"alias": "fileName"})
