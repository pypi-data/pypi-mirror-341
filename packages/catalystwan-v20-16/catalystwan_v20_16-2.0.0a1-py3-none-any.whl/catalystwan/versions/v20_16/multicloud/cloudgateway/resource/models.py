# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class CgwResourceResponseDetailsDevices:
    public_ip: Optional[str] = _field(default=None, metadata={"alias": "publicIp"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class CgwResourceResponseDetails:
    devices: Optional[List[CgwResourceResponseDetailsDevices]] = _field(default=None)
    vhub_name: Optional[str] = _field(default=None, metadata={"alias": "vhubName"})
    virtual_router_asn: Optional[str] = _field(default=None, metadata={"alias": "virtualRouterAsn"})
    vwan_name: Optional[str] = _field(default=None, metadata={"alias": "vwanName"})


@dataclass
class CgwResourceResponse:
    creation_date: Optional[str] = _field(default=None, metadata={"alias": "creationDate"})
    details: Optional[CgwResourceResponseDetails] = _field(default=None)
    esource_id: Optional[str] = _field(default=None, metadata={"alias": "esourceId"})
    resource_type: Optional[str] = _field(default=None, metadata={"alias": "resourceType"})
