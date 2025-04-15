# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import Literal

TemplateTypeParam = Literal[
    "app_usage",
    "executive_summary",
    "firewall_enforcement",
    "internet_browsing",
    "ips_events_collected",
    "link_availability",
    "link_sla",
    "link_utilization",
    "malware_files_collected",
    "site_availability",
]
