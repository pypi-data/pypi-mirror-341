# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass


@dataclass
class ApplicationSiteChartItem:
    entry_time: int
    qoe: int
