# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class MappingEntries:
    city_country: Optional[str] = _field(default=None, metadata={"alias": "CITY/COUNTRY"})
    fqdn: Optional[str] = _field(default=None, metadata={"alias": "FQDN"})
    ip: Optional[str] = _field(default=None, metadata={"alias": "IP"})


@dataclass
class GetDataCenters:
    mapping: Optional[List[MappingEntries]] = _field(default=None)
    title: Optional[str] = _field(default=None)
