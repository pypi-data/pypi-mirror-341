# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass


@dataclass
class SiteHealthTopologyItem:
    fair_site_count: int
    good_site_count: int
    poor_site_count: int
