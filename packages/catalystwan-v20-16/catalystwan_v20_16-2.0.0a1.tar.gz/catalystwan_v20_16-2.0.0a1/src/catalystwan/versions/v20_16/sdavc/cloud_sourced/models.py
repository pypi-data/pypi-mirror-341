# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class L3L4:
    clear_index: Optional[int] = _field(default=None, metadata={"alias": "clearIndex"})
    ip_addresses: Optional[List[str]] = _field(default=None, metadata={"alias": "ipAddresses"})
    l4_protocol: Optional[str] = _field(default=None, metadata={"alias": "l4Protocol"})
    ports: Optional[List[int]] = _field(default=None)


@dataclass
class ServerName:
    name: Optional[str] = _field(default=None)


@dataclass
class ApplicationDetails:
    app_name: Optional[str] = _field(default=None, metadata={"alias": "appName"})
    application_family: Optional[str] = _field(
        default=None, metadata={"alias": "applicationFamily"}
    )
    application_group: Optional[str] = _field(default=None, metadata={"alias": "applicationGroup"})
    business_relevance: Optional[str] = _field(
        default=None, metadata={"alias": "businessRelevance"}
    )
    cloud_sourced: Optional[str] = _field(default=None, metadata={"alias": "cloud-sourced"})
    common_name: Optional[str] = _field(default=None, metadata={"alias": "commonName"})
    id: Optional[str] = _field(default=None)
    l3_l4: Optional[List[L3L4]] = _field(default=None, metadata={"alias": "L3L4"})
    server_names: Optional[List[ServerName]] = _field(
        default=None, metadata={"alias": "serverNames"}
    )
    source_category: Optional[str] = _field(default=None, metadata={"alias": "sourceCategory"})
    status: Optional[str] = _field(default=None)
    traffic_class: Optional[str] = _field(default=None, metadata={"alias": "trafficClass"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class GetExtendedApplicationResponse:
    count: Optional[int] = _field(default=None)
    data: Optional[List[ApplicationDetails]] = _field(default=None)
    last_update_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdateOn"})


@dataclass
class DefaultSuccessResponse:
    message: Optional[str] = _field(default=None)
    success: Optional[bool] = _field(default=None)


@dataclass
class ApplicationRequestDetails:
    app_name: Optional[str] = _field(default=None, metadata={"alias": "appName"})


@dataclass
class SaveExtendedApplicationRequest:
    data: Optional[List[ApplicationRequestDetails]] = _field(default=None)
    select_all: Optional[bool] = _field(default=None, metadata={"alias": "selectAll"})
    update_network: Optional[bool] = _field(default=None, metadata={"alias": "updateNetwork"})
