# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class AnalyzeCliConfig:
    """
    Payload/body schema for analyze cli config
    """

    # device UUID
    device_uuid: str = _field(metadata={"alias": "deviceUuid"})
    # modeled cli config
    cli: Optional[str] = _field(default=None)
    # unmodeled cli config
    ioscli: Optional[str] = _field(default=None)
