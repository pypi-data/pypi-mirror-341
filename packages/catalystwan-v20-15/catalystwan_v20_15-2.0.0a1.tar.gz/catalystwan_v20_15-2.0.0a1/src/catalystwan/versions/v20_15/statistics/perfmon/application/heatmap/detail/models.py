# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from typing import Literal

LastNHoursParam = Literal["1", "12", "24", "3", "6"]


@dataclass
class ApplicationHeatMapDetail:
    fair_site: int
    good_site: int
    poor_site: int
