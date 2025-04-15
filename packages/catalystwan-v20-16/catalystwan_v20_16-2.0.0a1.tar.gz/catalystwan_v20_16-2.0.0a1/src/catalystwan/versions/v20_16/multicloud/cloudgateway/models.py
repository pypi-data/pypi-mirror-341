# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class CloudGatewayListResponse:
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    cloud_gateway_id: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayId"})
    cloud_gateway_name: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayName"})
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    custom_settings: Optional[bool] = _field(default=None, metadata={"alias": "customSettings"})
    description: Optional[str] = _field(default=None)
    region: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)


@dataclass
class Taskid:
    """
    Task id for polling status
    """

    id: Optional[str] = _field(default=None)


@dataclass
class CloudGatewayPostAzureProperties:
    """
    Used in Azure/Azure GovCloud CGW creation
    """

    resource_group_name: str = _field(metadata={"alias": "resourceGroupName"})
    resource_group_source: str = _field(metadata={"alias": "resourceGroupSource"})
    vhub_name: str = _field(metadata={"alias": "vhubName"})
    vhub_source: str = _field(metadata={"alias": "vhubSource"})
    vwan_name: str = _field(metadata={"alias": "vwanName"})
    vwan_source: str = _field(metadata={"alias": "vwanSource"})
    nva_source: Optional[str] = _field(default=None, metadata={"alias": "nvaSource"})
    vpn_gateway_source: Optional[str] = _field(default=None, metadata={"alias": "vpnGatewaySource"})


@dataclass
class CloudGatewayPostConfigGroupSettings:
    """
    Used in Azure/Azure GovCloud CGW creation
    """

    config_group_id: Optional[str] = _field(default=None, metadata={"alias": "configGroupId"})
    config_group_name: Optional[str] = _field(default=None, metadata={"alias": "configGroupName"})


@dataclass
class AllOfcloudGatewayPostSettings:
    cloud_gateway_solution: Optional[str] = _field(
        default=None, metadata={"alias": "cloudGatewaySolution"}
    )
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    instance_size: Optional[str] = _field(default=None, metadata={"alias": "instanceSize"})
    ip_subnet_pool: Optional[str] = _field(default=None, metadata={"alias": "ipSubnetPool"})
    name: Optional[str] = _field(default=None)
    # Used for GCP Custom settings
    network_tier: Optional[str] = _field(default=None, metadata={"alias": "networkTier"})
    # Used for Azure/Azure GovCloud Custom settings
    sku_scale_unit: Optional[str] = _field(default=None, metadata={"alias": "skuScaleUnit"})
    software_image_id: Optional[str] = _field(default=None, metadata={"alias": "softwareImageId"})
    # Tunnel Count for AWS Connect based and branch connect
    tunnel_count: Optional[str] = _field(default=None, metadata={"alias": "tunnelCount"})


@dataclass
class CloudGatewayPost:
    account_id: str = _field(metadata={"alias": "accountId"})
    # Used in Azure/Azure GovCloud CGW creation
    azure_properties: CloudGatewayPostAzureProperties = _field(
        metadata={"alias": "azureProperties"}
    )
    cloud_gateway_name: str = _field(metadata={"alias": "cloudGatewayName"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    cloud_gateway_mode: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayMode"})
    cloud_gateway_solution: Optional[str] = _field(
        default=None, metadata={"alias": "cloudGatewaySolution"}
    )
    cloud_gateway_tag: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayTag"})
    # Used in Azure/Azure GovCloud CGW creation
    config_group_settings: Optional[CloudGatewayPostConfigGroupSettings] = _field(
        default=None, metadata={"alias": "configGroupSettings"}
    )
    description: Optional[str] = _field(default=None)
    devices: Optional[List[str]] = _field(default=None)
    mrf_router_role: Optional[str] = _field(default=None, metadata={"alias": "mrfRouterRole"})
    region: Optional[str] = _field(default=None)
    s2s_permitted: Optional[str] = _field(default=None, metadata={"alias": "s2sPermitted"})
    settings: Optional[AllOfcloudGatewayPostSettings] = _field(default=None)
    site_name: Optional[str] = _field(default=None, metadata={"alias": "siteName"})
    ssh_key_name: Optional[str] = _field(default=None, metadata={"alias": "sshKeyName"})


@dataclass
class CustomSettings:
    cloud_gateway_solution: Optional[str] = _field(
        default=None, metadata={"alias": "cloudGatewaySolution"}
    )
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    instance_size: Optional[str] = _field(default=None, metadata={"alias": "instanceSize"})
    ip_subnet_pool: Optional[str] = _field(default=None, metadata={"alias": "ipSubnetPool"})
    name: Optional[str] = _field(default=None)
    # Used for GCP Custom settings
    network_tier: Optional[str] = _field(default=None, metadata={"alias": "networkTier"})
    # Used for Azure/Azure GovCloud Custom settings
    sku_scale_unit: Optional[str] = _field(default=None, metadata={"alias": "skuScaleUnit"})
    software_image_id: Optional[str] = _field(default=None, metadata={"alias": "softwareImageId"})
    # Tunnel Count for AWS Connect based and branch connect
    tunnel_count: Optional[str] = _field(default=None, metadata={"alias": "tunnelCount"})


@dataclass
class TunnelsInner:
    """
    CGW details relevant to AWS/AWS_GOVCLOUD
    """

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
    tunnel_inner_ip: Optional[List[str]] = _field(default=None, metadata={"alias": "tunnelInnerIp"})


@dataclass
class CloudGatewayAdjusted:
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    cloud_gateway_id: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayId"})
    # Only applicable to AWS/AWS_GOVCLOUD CloudTypes
    cloud_gateway_mode: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayMode"})
    cloud_gateway_name: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayName"})
    cloud_gateway_solution: Optional[str] = _field(
        default=None, metadata={"alias": "cloudGatewaySolution"}
    )
    # CGW details relevant to AWS/AWS_GOVCLOUD
    cloud_provider_asn: Optional[int] = _field(default=None, metadata={"alias": "cloudProviderASN"})
    # CGW details relevant to AWS/AWS_GOVCLOUD
    cloud_provider_mgmt_reference: Optional[str] = _field(
        default=None, metadata={"alias": "cloudProviderMgmtReference"}
    )
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    connected_sites: Optional[int] = _field(default=None, metadata={"alias": "connectedSites"})
    connectivity_state: Optional[str] = _field(
        default=None, metadata={"alias": "connectivityState"}
    )
    connectivity_state_update_ts: Optional[int] = _field(
        default=None, metadata={"alias": "connectivityStateUpdateTs"}
    )
    custom_settings: Optional[bool] = _field(default=None, metadata={"alias": "customSettings"})
    description: Optional[str] = _field(default=None)
    devices: Optional[List[str]] = _field(default=None)
    mrf_router_role: Optional[str] = _field(default=None, metadata={"alias": "mrfRouterRole"})
    region: Optional[str] = _field(default=None)
    # CGW details relevant to AZURE/AZURE_GOVCLOUD CloudTypes
    resource_group_name: Optional[str] = _field(
        default=None, metadata={"alias": "resourceGroupName"}
    )
    # CGW details relevant to AWS/AWS_GOVCLOUD
    route_table_count: Optional[str] = _field(default=None, metadata={"alias": "routeTableCount"})
    # Only applicable to GCP CloudGateways
    s2s_permitted: Optional[bool] = _field(default=None, metadata={"alias": "s2sPermitted"})
    settings: Optional[CustomSettings] = _field(default=None)
    site_name: Optional[str] = _field(default=None, metadata={"alias": "siteName"})
    status: Optional[str] = _field(default=None)
    # CGW details relevant to AWS/AWS_GOVCLOUD
    tunnel_cidr_blocks: Optional[List[Any]] = _field(
        default=None, metadata={"alias": "tunnelCidrBlocks"}
    )
    # CGW details relevant to AWS/AWS_GOVCLOUD
    tunnels: Optional[List[TunnelsInner]] = _field(default=None)
    # CGW details relevant to AZURE/AZURE_GOVCLOUD CloudTypes
    vhub_name: Optional[str] = _field(default=None, metadata={"alias": "vhubName"})
    # CGW details relevant to AZURE/AZURE_GOVCLOUD CloudTypes
    virtual_router_asn: Optional[str] = _field(default=None, metadata={"alias": "virtualRouterAsn"})
    vpns: Optional[List[str]] = _field(default=None)
    # CGW details relevant to AZURE/AZURE_GOVCLOUD CloudTypes
    vwan_name: Optional[str] = _field(default=None, metadata={"alias": "vwanName"})


@dataclass
class UpdateCgwDeviceChanges:
    """
    Used for GCP updateCgw
    """

    devices_added: Optional[List[str]] = _field(default=None, metadata={"alias": "devicesAdded"})
    devices_deleted: Optional[List[str]] = _field(
        default=None, metadata={"alias": "devicesDeleted"}
    )


@dataclass
class AllOfupdateCgwSettings:
    cloud_gateway_solution: Optional[str] = _field(
        default=None, metadata={"alias": "cloudGatewaySolution"}
    )
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    instance_size: Optional[str] = _field(default=None, metadata={"alias": "instanceSize"})
    ip_subnet_pool: Optional[str] = _field(default=None, metadata={"alias": "ipSubnetPool"})
    name: Optional[str] = _field(default=None)
    # Used for GCP Custom settings
    network_tier: Optional[str] = _field(default=None, metadata={"alias": "networkTier"})
    # Used for Azure/Azure GovCloud Custom settings
    sku_scale_unit: Optional[str] = _field(default=None, metadata={"alias": "skuScaleUnit"})
    software_image_id: Optional[str] = _field(default=None, metadata={"alias": "softwareImageId"})
    # Tunnel Count for AWS Connect based and branch connect
    tunnel_count: Optional[str] = _field(default=None, metadata={"alias": "tunnelCount"})


@dataclass
class UpdateCgw:
    account_id: str = _field(metadata={"alias": "accountId"})
    cloud_gateway_name: str = _field(metadata={"alias": "cloudGatewayName"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    region: str
    # Used for AZURE updateCgw
    resource_group_name: str = _field(metadata={"alias": "resourceGroupName"})
    # Used for AZURE updateCgw
    vhub_id: str = _field(metadata={"alias": "vhubId"})
    description: Optional[str] = _field(default=None)
    # Used for GCP updateCgw
    device_changes: Optional[UpdateCgwDeviceChanges] = _field(
        default=None, metadata={"alias": "deviceChanges"}
    )
    # Used for AZURE updateCgw
    devices: Optional[List[str]] = _field(default=None)
    mrf_router_role: Optional[str] = _field(default=None, metadata={"alias": "mrfRouterRole"})
    # Used for GCP updateCgw
    s2s_permitted: Optional[str] = _field(default=None, metadata={"alias": "s2sPermitted"})
    settings: Optional[AllOfupdateCgwSettings] = _field(default=None)
