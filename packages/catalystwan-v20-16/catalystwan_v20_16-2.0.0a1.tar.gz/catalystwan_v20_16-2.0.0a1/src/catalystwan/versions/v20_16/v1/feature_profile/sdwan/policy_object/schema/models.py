# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import Literal

SchemaTypeParam = Literal["post", "put"]

PolicyObjectListTypeParam = Literal[
    "app-list",
    "app-probe",
    "as-path",
    "class",
    "color",
    "data-ipv6-prefix",
    "data-prefix",
    "expanded-community",
    "ext-community",
    "ipv4-network-object-group",
    "ipv4-service-object-group",
    "ipv6-prefix",
    "mirror",
    "policer",
    "preferred-color-group",
    "prefix",
    "security-data-ip-prefix",
    "security-fqdn",
    "security-geolocation",
    "security-identity",
    "security-ipssignature",
    "security-localapp",
    "security-localdomain",
    "security-port",
    "security-protocolname",
    "security-scalablegrouptag",
    "security-urllist",
    "security-zone",
    "sla-class",
    "standard-community",
    "tloc",
    "vpn-group",
]
