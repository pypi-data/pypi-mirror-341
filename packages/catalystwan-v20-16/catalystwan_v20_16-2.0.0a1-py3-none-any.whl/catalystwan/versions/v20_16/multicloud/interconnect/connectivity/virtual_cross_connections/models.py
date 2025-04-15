# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class ProcessResponse:
    # Procees Id of the task
    id: Optional[str] = _field(default=None)


@dataclass
class AwsCloudDetail:
    """
    Interconnect cloud connect AWS cloud detail
    """

    # Interconnect cloud connect AWS cloud account id
    cloud_account_id: str = _field(metadata={"alias": "cloudAccountId"})
    # Interconnect cloud connect cloud account name
    cloud_account_name: str = _field(metadata={"alias": "cloudAccountName"})
    # Interconnect cloud connect AWS cross connect type
    cross_connect_type: str = _field(metadata={"alias": "crossConnectType"})
    # Interconnect cloud connect AWS cloud side BGP ASN
    cloud_side_bgp_asn: Optional[str] = _field(default=None, metadata={"alias": "cloudSideBgpAsn"})
    # Interconnect cloud connect AWS hosted connection id
    hosted_connection_id: Optional[str] = _field(
        default=None, metadata={"alias": "hostedConnectionId"}
    )
    # Interconnect cloud connect AWS hosted virtual interface id
    virtual_interface_id: Optional[str] = _field(
        default=None, metadata={"alias": "virtualInterfaceId"}
    )


@dataclass
class AzureCloudDetail:
    """
    Interconnect cloud connect Azure cloud detail
    """

    # Interconnect cloud connect Azure cloud account id
    cloud_account_id: str = _field(metadata={"alias": "cloudAccountId"})
    # Interconnect cloud connect cloud account name
    cloud_account_name: str = _field(metadata={"alias": "cloudAccountName"})
    # Interconnect cloud connect Azure cross connect type
    cross_connect_type: str = _field(metadata={"alias": "crossConnectType"})
    # Interconnect cloud connect Azure Express Route Circuit service key
    service_key: str = _field(metadata={"alias": "serviceKey"})


@dataclass
class GatewayDetail:
    """
    Interconnect connection end gateway detail
    """

    # Interconnect gateway name
    name: str
    # Interconnect gateway id
    id: Optional[str] = _field(default=None)
    # Interconnect gateway owner account id
    owner_id: Optional[str] = _field(default=None, metadata={"alias": "ownerId"})
    # Interconnect gateway region name
    region: Optional[str] = _field(default=None)
    # Interconnect gateway region id
    region_id: Optional[str] = _field(default=None, metadata={"alias": "regionId"})


@dataclass
class InterconnectInterfaceDetail:
    """
    Interconnect connection end interface detail
    """

    # BGP ASN of the connection end
    bgp_asn: Optional[str] = _field(default=None, metadata={"alias": "bgpAsn"})
    # BGP key of the connection end
    bgp_key: Optional[str] = _field(default=None, metadata={"alias": "bgpKey"})
    # Interface name of the connection end
    interface_name: Optional[str] = _field(default=None, metadata={"alias": "interfaceName"})
    # Interface IP address of the connection end
    ip_address: Optional[str] = _field(default=None, metadata={"alias": "ipAddress"})
    # MTU of the connection end
    mtu: Optional[str] = _field(default=None)
    # Interface IP address prefix of the connection end
    prefix: Optional[str] = _field(default=None)
    # VLAN ID of the connection end
    vlan_id: Optional[str] = _field(default=None, metadata={"alias": "vlanId"})


@dataclass
class PortDetail:
    """
    Interconnect connection end port detail
    """

    # Interconnect connection port id
    id: str
    # Interconnect connection port name
    name: str
    # Interconnect connection port owner account id
    owner_id: str = _field(metadata={"alias": "ownerId"})
    # Interconnect connection port region name
    region: str
    # Interconnect connection port region id
    region_id: str = _field(metadata={"alias": "regionId"})


@dataclass
class ConnectionEndDetail:
    """
    Interconnect device connect connection destination
    """

    # Interconnect connection end resource type
    resource_type: str = _field(metadata={"alias": "resourceType"})
    # Interconnect connection end gateway detail
    gateway_detail: Optional[GatewayDetail] = _field(
        default=None, metadata={"alias": "gatewayDetail"}
    )
    # Interconnect connection end interface detail
    interface_detail: Optional[InterconnectInterfaceDetail] = _field(
        default=None, metadata={"alias": "interfaceDetail"}
    )
    # Interconnect connection end port detail
    port_detail: Optional[PortDetail] = _field(default=None, metadata={"alias": "portDetail"})


@dataclass
class GoogleCloudDetail:
    """
    Interconnect cloud connect Google cloud detail
    """

    # Interconnect cloud connect cloud account name
    cloud_account_name: str = _field(metadata={"alias": "cloudAccountName"})
    # Google cross connect type
    cross_connect_type: str = _field(metadata={"alias": "crossConnectType"})
    # Google GCR attachment pairing key
    pairing_key: str = _field(metadata={"alias": "pairingKey"})
    # Google cloud account id
    cloud_account_id: Optional[str] = _field(default=None, metadata={"alias": "cloudAccountId"})


@dataclass
class CustomPeeringDetails:
    """
    Custom peering information for Interconnect cross connection destination
    """

    # Custom BGP ASN for a connection end
    bgp_asn: Optional[str] = _field(default=None, metadata={"alias": "bgpAsn"})
    # Custom ip address for a connection end
    ip_address: Optional[str] = _field(default=None, metadata={"alias": "ipAddress"})
    # Custom ip address prefix for a connection end
    prefix: Optional[str] = _field(default=None)


@dataclass
class CustomPeeringInfo:
    """
    Interconnect cross connection custom peering information
    """

    # Custom prefixes to be advertised to cloud for public connections
    advertised_prefixes: Optional[List[str]] = _field(
        default=None, metadata={"alias": "advertisedPrefixes"}
    )
    # Custom peering information for Interconnect cross connection destination
    destination_end: Optional[CustomPeeringDetails] = _field(
        default=None, metadata={"alias": "destinationEnd"}
    )
    # Custom peering information for Interconnect cross connection destination
    source_end: Optional[CustomPeeringDetails] = _field(
        default=None, metadata={"alias": "sourceEnd"}
    )


@dataclass
class InterconnectCrossConnectionPeeringInfo:
    """
    Interconnect device connect peering information
    """

    # Interconnect cross connection peering type
    peering_type: str = _field(metadata={"alias": "peeringType"})
    # Interconnect cross connection peering VPN segment
    vpn_segment: str = _field(metadata={"alias": "vpnSegment"})
    # Interconnect cross connection custom peering information
    custom_peering_info: Optional[CustomPeeringInfo] = _field(
        default=None, metadata={"alias": "customPeeringInfo"}
    )


@dataclass
class CloudConnectDetail:
    """
    Interconnect cross connection cloud connection detail
    """

    # Interconnect cloud connect cloud access type
    cloud_access_type: str = _field(metadata={"alias": "cloudAccessType"})
    # Interconnect cloud connect cloud provider type
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    # Interconnect device connect connection destination
    connection_destination: ConnectionEndDetail = _field(
        metadata={"alias": "connectionDestination"}
    )
    # Interconnect device connect connection destination
    connection_source: ConnectionEndDetail = _field(metadata={"alias": "connectionSource"})
    # Interconnect device connect peering information
    peering_info: InterconnectCrossConnectionPeeringInfo = _field(metadata={"alias": "peeringInfo"})
    # Interconnect cloud connect AWS cloud detail
    aws_cloud_detail: Optional[AwsCloudDetail] = _field(
        default=None, metadata={"alias": "awsCloudDetail"}
    )
    # Interconnect cloud connect Azure cloud detail
    azure_cloud_detail: Optional[AzureCloudDetail] = _field(
        default=None, metadata={"alias": "azureCloudDetail"}
    )
    # Interconnect cloud connect Google cloud detail
    google_cloud_detail: Optional[GoogleCloudDetail] = _field(
        default=None, metadata={"alias": "googleCloudDetail"}
    )
    # Interconnect cloud connect virtual network association type
    virtual_network_association_type: Optional[str] = _field(
        default=None, metadata={"alias": "virtualNetworkAssociationType"}
    )


@dataclass
class DeviceConnectDetail:
    """
    Interconnect cross connection device connection detail
    """

    # Interconnect device connect connection destination
    connection_destination: ConnectionEndDetail = _field(
        metadata={"alias": "connectionDestination"}
    )
    # Interconnect device connect connection destination
    connection_source: ConnectionEndDetail = _field(metadata={"alias": "connectionSource"})
    # Interconnect device connect peering information
    peering_info: InterconnectCrossConnectionPeeringInfo = _field(metadata={"alias": "peeringInfo"})


@dataclass
class InterconnectCrossConnectionLicenseDetail:
    """
    Interconnect cross connection license information
    """

    aws_hc_sku_end_date: Optional[str] = _field(default=None, metadata={"alias": "awsHcSkuEndDate"})
    aws_hc_sku_id: Optional[str] = _field(default=None, metadata={"alias": "awsHcSkuId"})
    end_date: Optional[str] = _field(default=None, metadata={"alias": "endDate"})
    max_licensed_bandwidth: Optional[str] = _field(
        default=None, metadata={"alias": "maxLicensedBandwidth"}
    )
    sku_id: Optional[str] = _field(default=None, metadata={"alias": "skuId"})


@dataclass
class RedundancyInfo:
    """
    Interconnect cross connection redundancy information
    """

    # Interconnect cross connection pair name
    connection_pair_name: str = _field(metadata={"alias": "connectionPairName"})
    # Interconnect cross connection pair id
    connection_pair_id: Optional[str] = _field(default=None, metadata={"alias": "connectionPairId"})


@dataclass
class ResourceAssociationDetail:
    associated_resource_connection_status: Optional[str] = _field(
        default=None, metadata={"alias": "associatedResourceConnectionStatus"}
    )
    associated_resource_id: Optional[str] = _field(
        default=None, metadata={"alias": "associatedResourceId"}
    )
    associated_resource_name: Optional[str] = _field(
        default=None, metadata={"alias": "associatedResourceName"}
    )
    associated_resource_status: Optional[str] = _field(
        default=None, metadata={"alias": "associatedResourceStatus"}
    )


@dataclass
class InterconnectResourceState:
    """
    Interconnect virtual network connection resource state information
    """

    resource_association_details: Optional[List[ResourceAssociationDetail]] = _field(
        default=None, metadata={"alias": "resourceAssociationDetails"}
    )
    resource_state: Optional[str] = _field(default=None, metadata={"alias": "resourceState"})
    resource_state_message: Optional[str] = _field(
        default=None, metadata={"alias": "resourceStateMessage"}
    )
    resource_state_update_ts: Optional[str] = _field(
        default=None, metadata={"alias": "resourceStateUpdateTs"}
    )


@dataclass
class InterconnectCrossConnection:
    # Interconnect cross connection id
    connection_id: str = _field(metadata={"alias": "connectionId"})
    # Interconnect cross connection name
    connection_name: str = _field(metadata={"alias": "connectionName"})
    # Interconnect cross connection role
    connection_role: str = _field(metadata={"alias": "connectionRole"})
    # Interconnect connectivity bandwidth
    connection_speed: str = _field(metadata={"alias": "connectionSpeed"})
    # Interconnect cross connection type
    connection_type: str = _field(metadata={"alias": "connectionType"})
    # Interconnect account id
    interconnect_account_id: str = _field(metadata={"alias": "interconnectAccountId"})
    # Interconnect provider type
    interconnect_type: str = _field(metadata={"alias": "interconnectType"})
    # Interconnect cross connection cloud connection detail
    cloud_connect_detail: Optional[CloudConnectDetail] = _field(
        default=None, metadata={"alias": "cloudConnectDetail"}
    )
    # Interconnect cross connection device connection detail
    device_connect_detail: Optional[DeviceConnectDetail] = _field(
        default=None, metadata={"alias": "deviceConnectDetail"}
    )
    # Interconnect cross connection license information
    license_detail: Optional[InterconnectCrossConnectionLicenseDetail] = _field(
        default=None, metadata={"alias": "licenseDetail"}
    )
    # Interconnect cross connection license type
    license_type: Optional[str] = _field(default=None, metadata={"alias": "licenseType"})
    # Interconnect cross connection redundancy information
    redundancy_info: Optional[RedundancyInfo] = _field(
        default=None, metadata={"alias": "redundancyInfo"}
    )
    # Interconnect virtual network connection resource state information
    resource_state: Optional[InterconnectResourceState] = _field(
        default=None, metadata={"alias": "resourceState"}
    )
