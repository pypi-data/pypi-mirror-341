# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class Prefixinfo:
    owned: Optional[List[str]] = _field(default=None)


@dataclass
class Regioninfo:
    id: Optional[int] = _field(default=None)
    name: Optional[str] = _field(default=None)
    responder_fqdn: Optional[str] = _field(default=None)


@dataclass
class RegionPrefixinfo:
    prefixes: Optional[Prefixinfo] = _field(default=None)
    region: Optional[Regioninfo] = _field(default=None)


@dataclass
class Configinfo:
    items: Optional[List[RegionPrefixinfo]] = _field(default=None)
    revision: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)


@dataclass
class WebexDataCenter:
    config: Optional[Configinfo] = _field(default=None)
    e_tag: Optional[str] = _field(default=None, metadata={"alias": "ETag"})
