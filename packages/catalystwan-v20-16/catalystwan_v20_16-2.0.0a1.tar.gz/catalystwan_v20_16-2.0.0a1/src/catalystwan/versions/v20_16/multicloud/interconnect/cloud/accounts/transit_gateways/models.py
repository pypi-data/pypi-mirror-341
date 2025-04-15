# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

CloudType = Literal["AWS", "AWS_GOVCLOUD", "AZURE", "AZURE_GOVCLOUD", "GCP"]

AssociationAction = Literal["ASSOCIATE", "DISASSOCIATE", "NO_ACTION", "REMOVE_PREFIX_LIST"]

ConnectionType = Literal["HCONN", "HVIF"]

VirtualInterfaceType = Literal["ATTACHMENT", "PRIVATE", "PUBLIC", "TRANSIT"]

PeeringState = Literal["DISABLED", "ENABLED"]

PeeringType = Literal["PRIVATE", "PUBLIC"]

ServiceProviderProvisioningState = Literal[
    "DEPROVISIONING", "NOT_PROVISIONED", "PROVISIONED", "PROVISIONING"
]

VirtualNetworkGatewayType = Literal["EXPRESS_ROUTE", "VPN"]

CloudTypeParam = Literal["AWS"]


@dataclass
class GatewayAssociationAssociatedGateway:
    """
    Cloud Connectivity Gateway Object
    """

    cloud_account_id: Optional[str] = _field(default=None, metadata={"alias": "cloudAccountId"})
    cloud_gateway_name: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayName"})
    cloud_type: Optional[CloudType] = _field(default=None, metadata={"alias": "cloudType"})
    description: Optional[str] = _field(default=None)
    gateway_id: Optional[str] = _field(default=None, metadata={"alias": "gatewayId"})
    gateway_name: Optional[str] = _field(default=None, metadata={"alias": "gatewayName"})
    region: Optional[str] = _field(default=None)


@dataclass
class GatewayAssociation:
    """
    Generic multicloud gateway association object
    """

    advertised_prefix_list: Optional[List[str]] = _field(
        default=None, metadata={"alias": "advertisedPrefixList"}
    )
    # Cloud Connectivity Gateway Object
    associated_gateway: Optional[GatewayAssociationAssociatedGateway] = _field(
        default=None, metadata={"alias": "associatedGateway"}
    )
    association_action: Optional[AssociationAction] = _field(
        default=None, metadata={"alias": "associationAction"}
    )
    association_id: Optional[str] = _field(default=None, metadata={"alias": "associationId"})
    association_state: Optional[str] = _field(default=None, metadata={"alias": "associationState"})
    state_change_error: Optional[str] = _field(default=None, metadata={"alias": "stateChangeError"})


@dataclass
class AwsDirectConnectGatewayVirtualInterfaceData:
    """
    VIrtual Interface Object
    """

    advertised_prefix_list: Optional[List[str]] = _field(
        default=None, metadata={"alias": "advertisedPrefixList"}
    )
    asn: Optional[int] = _field(default=None)
    bgp_key: Optional[str] = _field(default=None, metadata={"alias": "bgpKey"})
    customer_ip_address: Optional[str] = _field(
        default=None, metadata={"alias": "customerIpAddress"}
    )
    ip_address: Optional[str] = _field(default=None, metadata={"alias": "ipAddress"})
    vlan: Optional[int] = _field(default=None)


@dataclass
class AwsDirectConnectGatewayVirtualInterfaceAttachmentList:
    """
    Virtual Interface Object
    """

    attachment_state: Optional[str] = _field(default=None, metadata={"alias": "attachmentState"})
    cloud_type: Optional[CloudType] = _field(default=None, metadata={"alias": "cloudType"})
    # Id of the private cross connect
    connection_id: Optional[str] = _field(default=None, metadata={"alias": "connectionId"})
    # Type of AWS connection
    connection_type: Optional[ConnectionType] = _field(
        default=None, metadata={"alias": "connectionType"}
    )
    owner_account: Optional[str] = _field(default=None, metadata={"alias": "ownerAccount"})
    region: Optional[str] = _field(default=None)
    state_change_error: Optional[str] = _field(default=None, metadata={"alias": "stateChangeError"})
    # VIrtual Interface Object
    virtual_interface_data: Optional[AwsDirectConnectGatewayVirtualInterfaceData] = _field(
        default=None, metadata={"alias": "virtualInterfaceData"}
    )
    virtual_interface_id: Optional[str] = _field(
        default=None, metadata={"alias": "virtualInterfaceId"}
    )
    virtual_interface_name: Optional[str] = _field(
        default=None, metadata={"alias": "virtualInterfaceName"}
    )
    virtual_interface_type: Optional[VirtualInterfaceType] = _field(
        default=None, metadata={"alias": "virtualInterfaceType"}
    )


@dataclass
class AwsDirectConnectGateway:
    """
    AWS Direct Connect Gateway specific Object.
    """

    amazon_side_asn: str = _field(metadata={"alias": "amazonSideAsn"})
    # List of associated Gateways
    gateway_association_list: Optional[List[GatewayAssociation]] = _field(
        default=None, metadata={"alias": "gatewayAssociationList"}
    )
    owner_account: Optional[str] = _field(default=None, metadata={"alias": "ownerAccount"})
    # List of virtual interfaces attached to DxGW
    virtual_interface_attachment_list: Optional[
        List[AwsDirectConnectGatewayVirtualInterfaceAttachmentList]
    ] = _field(default=None, metadata={"alias": "virtualInterfaceAttachmentList"})
    # VPC Tags associated to the Direct Connect Gateway
    vpc_tag_names_for_gateway_associations: Optional[List[str]] = _field(
        default=None, metadata={"alias": "vpcTagNamesForGatewayAssociations"}
    )


@dataclass
class AwsVpcAttachments:
    """
    AWS VPC attachment Object
    """

    region: Optional[str] = _field(default=None)
    # VPC Id
    vpc_id: Optional[str] = _field(default=None, metadata={"alias": "vpcId"})
    # List of ip prefixes to be advertized towards DxGw on the VPC routing table.
    vpc_route_prefix_list: Optional[List[str]] = _field(
        default=None, metadata={"alias": "vpcRoutePrefixList"}
    )
    vpc_state: Optional[str] = _field(default=None, metadata={"alias": "vpcState"})
    # List of VPC subnets to be added to DxGw association.
    vpc_subnet_prefix_list: Optional[List[str]] = _field(
        default=None, metadata={"alias": "vpcSubnetPrefixList"}
    )


@dataclass
class AwsTransitGateway:
    """
    AWS Transit Gateway specific Object.
    """

    amazon_side_asn: str = _field(metadata={"alias": "amazonSideAsn"})
    association_default_route_table_id: Optional[str] = _field(
        default=None, metadata={"alias": "associationDefaultRouteTableId"}
    )
    auto_accept_shared_attachments: Optional[bool] = _field(
        default=None, metadata={"alias": "autoAcceptSharedAttachments"}
    )
    creation_time: Optional[str] = _field(default=None, metadata={"alias": "creationTime"})
    default_route_table_association: Optional[bool] = _field(
        default=None, metadata={"alias": "defaultRouteTableAssociation"}
    )
    default_route_table_propogation: Optional[bool] = _field(
        default=None, metadata={"alias": "defaultRouteTablePropogation"}
    )
    dns_support: Optional[bool] = _field(default=None, metadata={"alias": "dnsSupport"})
    multicast_support: Optional[bool] = _field(default=None, metadata={"alias": "multicastSupport"})
    owner_account: Optional[str] = _field(default=None, metadata={"alias": "ownerAccount"})
    propogation_default_route_table_id: Optional[str] = _field(
        default=None, metadata={"alias": "propogationDefaultRouteTableId"}
    )
    # List of VPC attachments
    vpc_attachment_list: Optional[List[AwsVpcAttachments]] = _field(
        default=None, metadata={"alias": "vpcAttachmentList"}
    )
    vpn_ecmp_support: Optional[bool] = _field(default=None, metadata={"alias": "vpnEcmpSupport"})


@dataclass
class AwsVirtualPrivateGateway:
    """
    AWS Virtual Private Gateway specific Object.
    """

    amazon_side_asn: Optional[int] = _field(default=None, metadata={"alias": "amazonSideAsn"})
    availability_zone: Optional[str] = _field(default=None, metadata={"alias": "availabilityZone"})
    # List of VPC attachments
    vpc_attachment_list: Optional[List[AwsVpcAttachments]] = _field(
        default=None, metadata={"alias": "vpcAttachmentList"}
    )
    vpg_type: Optional[str] = _field(default=None, metadata={"alias": "vpgType"})


@dataclass
class CloudConnectivityGatewayAws:
    """
    AWS cloud Connectivity Gateway Object
    """

    aws_connectivity_type: str = _field(metadata={"alias": "awsConnectivityType"})
    # AWS Direct Connect Gateway specific Object.
    direct_connect_gateway: Optional[AwsDirectConnectGateway] = _field(
        default=None, metadata={"alias": "directConnectGateway"}
    )
    # AWS Transit Gateway specific Object.
    transit_gateway: Optional[AwsTransitGateway] = _field(
        default=None, metadata={"alias": "transitGateway"}
    )
    # AWS Virtual Private Gateway specific Object.
    virtual_private_gateway: Optional[AwsVirtualPrivateGateway] = _field(
        default=None, metadata={"alias": "virtualPrivateGateway"}
    )


@dataclass
class AzureErcPeering:
    """
    Azure Express Route Circuit Peering
    """

    advertised_public_prefix_list: Optional[List[str]] = _field(
        default=None, metadata={"alias": "advertisedPublicPrefixList"}
    )
    azure_asn: Optional[str] = _field(default=None, metadata={"alias": "azureAsn"})
    express_route_connection_id: Optional[str] = _field(
        default=None, metadata={"alias": "expressRouteConnectionId"}
    )
    id: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    peer_asn: Optional[str] = _field(default=None, metadata={"alias": "peerAsn"})
    peering_state: Optional[PeeringState] = _field(default=None, metadata={"alias": "peeringState"})
    peering_type: Optional[PeeringType] = _field(default=None, metadata={"alias": "peeringType"})
    primary_azure_port: Optional[str] = _field(default=None, metadata={"alias": "primaryAzurePort"})
    primary_peer_address_prefix: Optional[str] = _field(
        default=None, metadata={"alias": "primaryPeerAddressPrefix"}
    )
    secondary_azure_port: Optional[str] = _field(
        default=None, metadata={"alias": "secondaryAzurePort"}
    )
    secondary_peer_address_prefix: Optional[str] = _field(
        default=None, metadata={"alias": "secondaryPeerAddressPrefix"}
    )
    # BGP Peering Key
    shared_key: Optional[str] = _field(default=None, metadata={"alias": "sharedKey"})
    vlan_id: Optional[int] = _field(default=None, metadata={"alias": "vlanId"})


@dataclass
class AzureErcServiceProviderProperties:
    """
    Azure Express Route Circuit Service Provider Properties
    """

    bandwidth_in_mbps: Optional[int] = _field(default=None, metadata={"alias": "bandwidthInMbps"})
    peering_location: Optional[str] = _field(default=None, metadata={"alias": "peeringLocation"})
    service_provider_name: Optional[str] = _field(
        default=None, metadata={"alias": "serviceProviderName"}
    )


@dataclass
class AzureExpressRouteCircuitSku:
    """
    Express Route Circuit SKU
    """

    family: str
    tier: str
    name: Optional[str] = _field(default=None)


@dataclass
class AzureVirtualWanTagList:
    """
    Azure Virtual WAN Tag Object
    """

    name: Optional[str] = _field(default=None)
    value: Optional[str] = _field(default=None)


@dataclass
class AzureVirtualHubVirtualRouterIp:
    """
    Virtual Router IP
    """

    private_ip: Optional[str] = _field(default=None, metadata={"alias": "privateIp"})


@dataclass
class AzureVirtualHub:
    """
    Azure Virtual Hub
    """

    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    address_prefix: Optional[str] = _field(default=None, metadata={"alias": "addressPrefix"})
    cloud_type: Optional[CloudType] = _field(default=None, metadata={"alias": "cloudType"})
    id: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    provisioning_state: Optional[str] = _field(
        default=None, metadata={"alias": "provisioningState"}
    )
    region: Optional[str] = _field(default=None)
    resource_group_name: Optional[str] = _field(
        default=None, metadata={"alias": "resourceGroupName"}
    )
    routing_state: Optional[str] = _field(default=None, metadata={"alias": "routingState"})
    sku: Optional[str] = _field(default=None)
    tag_list: Optional[List[AzureVirtualWanTagList]] = _field(
        default=None, metadata={"alias": "tagList"}
    )
    virtual_router_asn: Optional[str] = _field(default=None, metadata={"alias": "virtualRouterAsn"})
    virtual_router_ip: Optional[List[AzureVirtualHubVirtualRouterIp]] = _field(
        default=None, metadata={"alias": "virtualRouterIp"}
    )
    vwan_name: Optional[str] = _field(default=None, metadata={"alias": "vwanName"})


@dataclass
class AzureExpressRouteCircuitVHubList:
    is_delete: Optional[bool] = _field(default=None, metadata={"alias": "isDelete"})
    # Azure Virtual Hub
    v_hub: Optional[AzureVirtualHub] = _field(default=None, metadata={"alias": "vHub"})


@dataclass
class AzureVirtualWan:
    """
    Azure Virtual Wan
    """

    name: str
    region: str
    resource_group_name: str = _field(metadata={"alias": "resourceGroupName"})
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    # Cloud account name
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    allow_branch_to_branch_traffic: Optional[bool] = _field(
        default=None, metadata={"alias": "allowBranchToBranchTraffic"}
    )
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    description: Optional[str] = _field(default=None)
    id: Optional[str] = _field(default=None)
    provisioning_state: Optional[str] = _field(
        default=None, metadata={"alias": "provisioningState"}
    )
    tag_list: Optional[List[AzureVirtualWanTagList]] = _field(
        default=None, metadata={"alias": "tagList"}
    )
    virtual_wan_type: Optional[str] = _field(default=None, metadata={"alias": "virtualWanType"})
    vnet_tovnet_traffic_enabled: Optional[bool] = _field(
        default=None, metadata={"alias": "vnetTovnetTrafficEnabled"}
    )


@dataclass
class AzureExpressRouteCircuitVWanAttachmentList:
    """
    vWan Attachment Name
    """

    v_hub_list: Optional[List[AzureExpressRouteCircuitVHubList]] = _field(
        default=None, metadata={"alias": "vHubList"}
    )
    # Azure Virtual Wan
    v_wan: Optional[AzureVirtualWan] = _field(default=None, metadata={"alias": "vWan"})


@dataclass
class AzureExpressRouteCircuitVnetTagNamesForConnections:
    """
    Vnet Tag Object Names
    """

    is_delete: Optional[bool] = _field(default=None, metadata={"alias": "isDelete"})
    vnet_tag_name: Optional[str] = _field(default=None, metadata={"alias": "vnetTagName"})


@dataclass
class AzureExpressRouteCircuit:
    """
    Azure Express Route Circuit Object
    """

    resource_group_name: str = _field(metadata={"alias": "resourceGroupName"})
    allow_classic_operations: Optional[bool] = _field(
        default=None, metadata={"alias": "allowClassicOperations"}
    )
    bandwidth_in_gbps: Optional[int] = _field(default=None, metadata={"alias": "bandwidthInGbps"})
    gateway_association_list: Optional[List[GatewayAssociation]] = _field(
        default=None, metadata={"alias": "gatewayAssociationList"}
    )
    global_reach_enabled: Optional[bool] = _field(
        default=None, metadata={"alias": "globalReachEnabled"}
    )
    peering_list: Optional[List[AzureErcPeering]] = _field(
        default=None, metadata={"alias": "peeringList"}
    )
    provisioning_state: Optional[str] = _field(
        default=None, metadata={"alias": "provisioningState"}
    )
    service_key: Optional[str] = _field(default=None, metadata={"alias": "serviceKey"})
    # Azure Express Route Circuit Service Provider Properties
    service_provider_properties: Optional[AzureErcServiceProviderProperties] = _field(
        default=None, metadata={"alias": "serviceProviderProperties"}
    )
    service_provider_provisioning_state: Optional[ServiceProviderProvisioningState] = _field(
        default=None, metadata={"alias": "serviceProviderProvisioningState"}
    )
    # Express Route Circuit SKU
    sku: Optional[AzureExpressRouteCircuitSku] = _field(default=None)
    v_wan_attachment_list: Optional[List[AzureExpressRouteCircuitVWanAttachmentList]] = _field(
        default=None, metadata={"alias": "vWanAttachmentList"}
    )
    vnet_tag_names_for_connections: Optional[
        List[AzureExpressRouteCircuitVnetTagNamesForConnections]
    ] = _field(default=None, metadata={"alias": "vnetTagNamesForConnections"})


@dataclass
class AzureExpressRouteGateway:
    """
    Azure Express Route Gateway Object
    """

    auto_scale_configuration: Optional[str] = _field(
        default=None, metadata={"alias": "autoScaleConfiguration"}
    )
    resource_group_name: Optional[str] = _field(
        default=None, metadata={"alias": "resourceGroupName"}
    )
    # Id of the Azure vHUB.
    v_hub_id: Optional[str] = _field(default=None, metadata={"alias": "vHubId"})


@dataclass
class AzureVirtualNetworkGatewaySku:
    """
    VNET Gateway SKU parameters
    """

    capacity: Optional[int] = _field(default=None)
    name: Optional[str] = _field(default=None)
    tier: Optional[str] = _field(default=None)


@dataclass
class AzureVirtualNetworkGateway:
    """
    Azure Virtual Network Gateway Object
    """

    enable_bgp: Optional[bool] = _field(default=None, metadata={"alias": "enableBgp"})
    public_ip_address: Optional[str] = _field(default=None, metadata={"alias": "publicIPAddress"})
    # VNET Gateway SKU parameters
    sku: Optional[AzureVirtualNetworkGatewaySku] = _field(default=None)
    subnet: Optional[str] = _field(default=None)
    virtual_network_gateway_type: Optional[VirtualNetworkGatewayType] = _field(
        default=None, metadata={"alias": "virtualNetworkGatewayType"}
    )


@dataclass
class CloudConnectivityGatewayAzure:
    """
    Cloud Connectivity Gateway Object
    """

    azure_connectivity_type: str = _field(metadata={"alias": "azureConnectivityType"})
    # Azure Express Route Circuit Object
    express_route_circuit: Optional[AzureExpressRouteCircuit] = _field(
        default=None, metadata={"alias": "expressRouteCircuit"}
    )
    # Azure Express Route Gateway Object
    express_route_gateway: Optional[AzureExpressRouteGateway] = _field(
        default=None, metadata={"alias": "expressRouteGateway"}
    )
    # Azure Virtual Network Gateway Object
    virtual_network_gateway: Optional[AzureVirtualNetworkGateway] = _field(
        default=None, metadata={"alias": "virtualNetworkGateway"}
    )


@dataclass
class GcpInterconnectAttachment:
    """
    Google cloud Interconnect Attachment Object.
    """

    cloud_router_ip_address: Optional[str] = _field(
        default=None, metadata={"alias": "cloudRouterIpAddress"}
    )
    customer_ip_address: Optional[str] = _field(
        default=None, metadata={"alias": "customerIpAddress"}
    )
    id: Optional[str] = _field(default=None)
    # MTU of the Interconnect attachment
    mtu: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    pairing_key: Optional[str] = _field(default=None, metadata={"alias": "pairingKey"})
    region: Optional[str] = _field(default=None)
    # Option to create Interconnect attachment in secondary zone
    secondary_zone: Optional[str] = _field(default=None, metadata={"alias": "secondaryZone"})
    state: Optional[str] = _field(default=None)


@dataclass
class GcpCloudRouter:
    """
    Google cloud GCR Object.
    """

    name: str
    network: str
    # List of GCR Attachments
    attachment_details: Optional[List[GcpInterconnectAttachment]] = _field(
        default=None, metadata={"alias": "attachmentDetails"}
    )
    cloud_router_asn: Optional[str] = _field(default=None, metadata={"alias": "cloudRouterAsn"})
    id: Optional[str] = _field(default=None)
    region: Optional[str] = _field(default=None)


@dataclass
class CloudConnectivityGatewayGcp:
    """
    Google cloud Connectivity Gateway Object.
    """

    gc_connectivity_type: str = _field(metadata={"alias": "gcConnectivityType"})
    # Google cloud GCR Object.
    router_info: GcpCloudRouter = _field(metadata={"alias": "routerInfo"})
    # BGP ASN assigned to Interconnect Gateway.
    interconnect_asn: Optional[str] = _field(default=None, metadata={"alias": "interconnectAsn"})
    pairing_key: Optional[str] = _field(default=None, metadata={"alias": "pairingKey"})


@dataclass
class CloudConnectivityGateway:
    """
    Cloud Connectivity Gateway Object
    """

    # AWS cloud Connectivity Gateway Object
    aws_connectivity_gateway: CloudConnectivityGatewayAws = _field(
        metadata={"alias": "awsConnectivityGateway"}
    )
    # Cloud Connectivity Gateway Object
    azure_connectivity_gateway: CloudConnectivityGatewayAzure = _field(
        metadata={"alias": "azureConnectivityGateway"}
    )
    cloud_account_id: str = _field(metadata={"alias": "cloudAccountId"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    gateway_name: str = _field(metadata={"alias": "gatewayName"})
    # Google cloud Connectivity Gateway Object.
    gcp_connectivity_gateway: CloudConnectivityGatewayGcp = _field(
        metadata={"alias": "gcpConnectivityGateway"}
    )
    region: str
    cloud_gateway_name: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayName"})
    connectivity_gateway_state: Optional[str] = _field(
        default=None, metadata={"alias": "connectivityGatewayState"}
    )
    description: Optional[str] = _field(default=None)
    gateway_id: Optional[str] = _field(default=None, metadata={"alias": "gatewayId"})
    # Resource created by vManage
    is_vmanage_created: Optional[bool] = _field(
        default=None, metadata={"alias": "isVmanageCreated"}
    )
    # Option indicates object type
    new_format: Optional[bool] = _field(default=None, metadata={"alias": "newFormat"})


@dataclass
class InlineResponse2008:
    """
    Cloud Connectivity Gateway Object
    """

    connectivity_gateway: Optional[List[CloudConnectivityGateway]] = _field(
        default=None, metadata={"alias": "connectivityGateway"}
    )
