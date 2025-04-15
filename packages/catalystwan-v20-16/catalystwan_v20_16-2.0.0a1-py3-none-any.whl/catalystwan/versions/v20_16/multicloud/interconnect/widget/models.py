# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

EdgeGatewaySolution = Literal["MVE", "NE"]

EdgeType = Literal["EQUINIX", "MEGAPORT"]


@dataclass
class StatusObject:
    count: Optional[int] = _field(default=None)
    message: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)


@dataclass
class GwDeviceStatus:
    count: Optional[int] = _field(default=None)
    name: Optional[str] = _field(default=None)
    status_list: Optional[List[StatusObject]] = _field(
        default=None, metadata={"alias": "statusList"}
    )
    unreachable_count: Optional[int] = _field(default=None, metadata={"alias": "unreachableCount"})


@dataclass
class GwSiteStatus:
    count: Optional[int] = _field(default=None)
    name: Optional[str] = _field(default=None)
    status_list: Optional[List[StatusObject]] = _field(
        default=None, metadata={"alias": "statusList"}
    )


@dataclass
class GwStatus:
    count: Optional[int] = _field(default=None)
    name: Optional[str] = _field(default=None)
    status_list: Optional[List[StatusObject]] = _field(
        default=None, metadata={"alias": "statusList"}
    )


@dataclass
class InterconnectWidget:
    edge_gateway_solution: Optional[EdgeGatewaySolution] = _field(
        default=None, metadata={"alias": "edgeGatewaySolution"}
    )
    edge_type: Optional[EdgeType] = _field(default=None, metadata={"alias": "edgeType"})
    gw_device_site_ids: Optional[List[int]] = _field(
        default=None, metadata={"alias": "gwDeviceSiteIds"}
    )
    gw_device_status: Optional[GwDeviceStatus] = _field(
        default=None, metadata={"alias": "gwDeviceStatus"}
    )
    gw_sitestatus: Optional[GwSiteStatus] = _field(default=None, metadata={"alias": "gwSitestatus"})
    gw_status: Optional[GwStatus] = _field(default=None, metadata={"alias": "gwStatus"})
    num_accounts: Optional[int] = _field(default=None, metadata={"alias": "numAccounts"})
    num_conn: Optional[int] = _field(default=None, metadata={"alias": "numConn"})
    num_sdwan_tunnels: Optional[int] = _field(default=None, metadata={"alias": "numSdwanTunnels"})
