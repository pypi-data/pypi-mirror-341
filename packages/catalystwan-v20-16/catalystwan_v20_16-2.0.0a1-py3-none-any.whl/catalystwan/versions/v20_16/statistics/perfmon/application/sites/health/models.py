# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from typing import Literal

LastNHoursParam = Literal["1", "12", "24", "3", "6"]

HealthParam = Literal["FAIR", "GOOD", "POOR"]


@dataclass
class ApplicationSitesItem:
    fair_path: int
    good_path: int
    health: str
    poor_path: int
    siteid: str
