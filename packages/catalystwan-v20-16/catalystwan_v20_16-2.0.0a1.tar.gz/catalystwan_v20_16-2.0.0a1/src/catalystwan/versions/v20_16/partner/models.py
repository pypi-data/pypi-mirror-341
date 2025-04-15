# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

Type = Literal["aci", "dnac", "mdp", "wcm"]


@dataclass
class PartnerRes:
    description: Optional[str] = _field(default=None)
    devices_attached: Optional[int] = _field(default=None, metadata={"alias": "devicesAttached"})
    id: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    owner: Optional[str] = _field(default=None)
    partner_id: Optional[str] = _field(default=None, metadata={"alias": "partnerId"})
    registration_date: Optional[int] = _field(default=None, metadata={"alias": "registrationDate"})
    type_: Optional[Type] = _field(default=None, metadata={"alias": "type"})


@dataclass
class RegisterPartnerRes:
    id: Optional[str] = _field(default=None)


@dataclass
class RegisterPartnerRequest:
    description: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    partner_id: Optional[str] = _field(default=None, metadata={"alias": "partnerId"})


@dataclass
class UpdatePartnerRequest:
    description: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class StatusResponse:
    status: Optional[str] = _field(default=None)
