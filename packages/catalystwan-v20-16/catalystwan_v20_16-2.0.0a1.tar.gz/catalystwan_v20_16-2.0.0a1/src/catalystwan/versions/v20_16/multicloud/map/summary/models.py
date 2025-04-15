# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

CloudTypeParam = Literal["AWS", "AWS_GOVCLOUD", "AZURE", "AZURE_GOVCLOUD", "GCP"]


@dataclass
class MapSummaryAccountId:
    site_to_cloud_ncc_hub_name: Optional[str] = _field(
        default=None, metadata={"alias": "Site To Cloud NCC Hub Name"}
    )
    site_to_cloud_ncc_spoke_name: Optional[str] = _field(
        default=None, metadata={"alias": "Site To Cloud NCC Spoke Name"}
    )
    site_to_cloud_primary_gcr_name: Optional[str] = _field(
        default=None, metadata={"alias": "Site To Cloud Primary GCR Name"}
    )
    site_to_cloud_vpc_id: Optional[str] = _field(
        default=None, metadata={"alias": "Site To Cloud VPC ID"}
    )
    site_to_cloud_vpc_name: Optional[str] = _field(
        default=None, metadata={"alias": "Site To Cloud VPC Name"}
    )
    site_to_site_ncc_hub_name: Optional[str] = _field(
        default=None, metadata={"alias": "Site To Site NCC Hub Name"}
    )
    site_to_site_vpc_id: Optional[str] = _field(
        default=None, metadata={"alias": "Site To Site VPC ID"}
    )
    site_to_site_vpc_name: Optional[str] = _field(
        default=None, metadata={"alias": "Site To Site VPC Name"}
    )
    wan_vpc_id: Optional[str] = _field(default=None, metadata={"alias": "WAN VPC ID"})
    wan_vpc_name: Optional[str] = _field(default=None, metadata={"alias": "WAN VPC Name"})


@dataclass
class MapSummaryDevices:
    reachability: Optional[str] = _field(default=None)
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "systemIp"})
    uuid: Optional[str] = _field(default=None)


@dataclass
class MapSummaryHostVpcs:
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    host_vpc_id: Optional[str] = _field(default=None, metadata={"alias": "hostVpcId"})
    tag: Optional[str] = _field(default=None)


@dataclass
class MapSummaryTags:
    tag: Optional[str] = _field(default=None)


@dataclass
class MapSummaryTunnels:
    accepted_route_count: Optional[int] = _field(
        default=None, metadata={"alias": "acceptedRouteCount"}
    )
    last_status_change_timestamp: Optional[str] = _field(
        default=None, metadata={"alias": "lastStatusChangeTimestamp"}
    )
    outer_ip_addr: Optional[str] = _field(default=None, metadata={"alias": "outerIpAddr"})
    status: Optional[str] = _field(default=None)
    status_message: Optional[str] = _field(default=None, metadata={"alias": "statusMessage"})
    tunnel_id: Optional[str] = _field(default=None, metadata={"alias": "tunnelId"})


@dataclass
class MapSummaryVpns:
    vpn_id: Optional[str] = _field(default=None, metadata={"alias": "vpnId"})


@dataclass
class MapSummary:
    account_id: Optional[MapSummaryAccountId] = _field(
        default=None, metadata={"alias": "Account ID"}
    )
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    additional_details: Optional[str] = _field(
        default=None, metadata={"alias": "additionalDetails"}
    )
    azure_virtual_wan_hub_id: Optional[str] = _field(
        default=None, metadata={"alias": "Azure Virtual WAN Hub ID"}
    )
    cloud_gateway_name: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayName"})
    cloud_gateway_solution: Optional[str] = _field(
        default=None, metadata={"alias": "cloudGatewaySolution"}
    )
    cloud_provider_mgmt_reference: Optional[str] = _field(
        default=None, metadata={"alias": "cloudProviderMgmtReference"}
    )
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    connected_sites: Optional[int] = _field(default=None, metadata={"alias": "connectedSites"})
    connectivity_state: Optional[str] = _field(
        default=None, metadata={"alias": "connectivityState"}
    )
    connectivity_state_update_ts: Optional[str] = _field(
        default=None, metadata={"alias": "connectivityStateUpdateTs"}
    )
    devices: Optional[List[MapSummaryDevices]] = _field(default=None)
    host_vpcs: Optional[MapSummaryHostVpcs] = _field(default=None, metadata={"alias": "hostVpcs"})
    oper_state: Optional[str] = _field(default=None, metadata={"alias": "operState"})
    region: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)
    tags: Optional[MapSummaryTags] = _field(default=None)
    tunnels: Optional[List[MapSummaryTunnels]] = _field(default=None)
    vpns: Optional[MapSummaryVpns] = _field(default=None)
