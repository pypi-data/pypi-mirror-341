# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

ValueType = Literal["ARRAY", "FALSE", "NULL", "NUMBER", "OBJECT", "STRING", "TRUE"]


@dataclass
class DirectConnectGatewayDetails:
    """
    Interconnect OnRamp gateway connection Direct connect gateway details
    """

    # Interconnect OnRamp AWS Direct Connect Gateway cloud resource id
    cloud_resource_id: str = _field(metadata={"alias": "cloudResourceId"})
    # Interconnect On Ramp AWS Direct Connect Gateway cloud resource id
    id: Optional[str] = _field(default=None)
    # Interconnect On Ramp AWS Direct Connect Gateway cloud resource name
    name: Optional[str] = _field(default=None)


@dataclass
class ExpressRouteCircuitDetails:
    """
    Interconnect OnRamp gateway connection Express route circuit details
    """

    # Interconnect OnRamp Azure express route circuit cloud resource id
    cloud_resource_id: str = _field(metadata={"alias": "cloudResourceId"})
    # Interconnect OnRamp Azure express route circuit id
    id: Optional[str] = _field(default=None)
    # Interconnect OnRamp Azure express route circuit name
    name: Optional[str] = _field(default=None)
    # Interconnect OnRamp Azure express route circuit resource group
    resource_group_name: Optional[str] = _field(
        default=None, metadata={"alias": "resourceGroupName"}
    )
    # Interconnect OnRamp Azure express route circuit service key
    service_key: Optional[str] = _field(default=None, metadata={"alias": "serviceKey"})


@dataclass
class CgwDetails:
    """
    Interconnect OnRamp gateway association MultiCloud gateway details
    """

    # Interconnect On Ramp Gateway connection cloud connect cloud account id
    cloud_account_id: str = _field(metadata={"alias": "cloudAccountId"})
    # Interconnect OnRamp gateway associated cgw gateway name
    name: str
    # Interconnect on ramp gateway connection cgw advertised prefixes
    advertised_prefixes: Optional[List[str]] = _field(
        default=None, metadata={"alias": "advertisedPrefixes"}
    )
    # Interconnect OnRamp gateway associated cgw gateway id
    id: Optional[str] = _field(default=None)


@dataclass
class TgwDetails:
    """
    Interconnect OnRamp gateway association Transit gateway details
    """

    # Prefixes to be advertised to the Direct Connect Gateway
    advertised_prefixes: List[str] = _field(metadata={"alias": "advertisedPrefixes"})
    # Transit gateway cloud account id
    cloud_account_id: str = _field(metadata={"alias": "cloudAccountId"})
    # Transit gateway create flag
    is_create: str = _field(metadata={"alias": "isCreate"})
    # Transit Gateway cloud side BGP ASN
    bgp_asn: Optional[str] = _field(default=None, metadata={"alias": "bgpAsn"})
    # Transit gateway cloud resource id
    cloud_resource_id: Optional[str] = _field(default=None, metadata={"alias": "cloudResourceId"})
    create: Optional[bool] = _field(default=None)
    # Transit gateway id
    id: Optional[str] = _field(default=None)
    # Transit gateway name
    name: Optional[str] = _field(default=None)
    # Transit gateway region
    region: Optional[str] = _field(default=None)


@dataclass
class VhubDetails:
    """
    Interconnect OnRamp gateway association Virtual hub details
    """

    # Virtual hub gateway address prefix
    address_prefix: str = _field(metadata={"alias": "addressPrefix"})
    # Virtual hub gateway cloud account id
    cloud_account_id: str = _field(metadata={"alias": "cloudAccountId"})
    # Virtual hub gateway create flag
    is_create: str = _field(metadata={"alias": "isCreate"})
    # Virtual hub gateway cloud resource id
    cloud_resource_id: Optional[str] = _field(default=None, metadata={"alias": "cloudResourceId"})
    create: Optional[bool] = _field(default=None)
    # Virtual hub gateway id
    id: Optional[str] = _field(default=None)
    # Virtual hub gateway name
    name: Optional[str] = _field(default=None)
    # Virtual hub gateway region
    region: Optional[str] = _field(default=None)
    # Virtual hub gateway resource group
    resource_group_name: Optional[str] = _field(
        default=None, metadata={"alias": "resourceGroupName"}
    )


@dataclass
class GatewayAssociationDetail:
    """
    Interconnect OnRamp gateway connection gateway associations
    """

    # Interconnect OnRamp gateway association type
    resource_type: str = _field(metadata={"alias": "resourceType"})
    # Interconnect OnRamp gateway association MultiCloud gateway details
    cgw_details: Optional[CgwDetails] = _field(default=None, metadata={"alias": "cgwDetails"})
    # Interconnect OnRamp gateway association Transit gateway details
    tgw_details: Optional[TgwDetails] = _field(default=None, metadata={"alias": "tgwDetails"})
    # Interconnect OnRamp gateway association Virtual hub details
    vhub_details: Optional[VhubDetails] = _field(default=None, metadata={"alias": "vhubDetails"})


@dataclass
class GoogleCloudRouterDetails:
    """
    Interconnect OnRamp gateway connection Google cloud router details
    """

    # Interconnect OnRamp Google cloud router & attachment cloud resource id
    cloud_resource_id: str = _field(metadata={"alias": "cloudResourceId"})
    # Interconnect OnRamp Google cloud router & attachment role
    role: str
    # Interconnect OnRamp Google cloud router attachment detail
    google_attachment_detail: Optional[str] = _field(
        default=None, metadata={"alias": "googleAttachmentDetail"}
    )
    # Interconnect OnRamp Google cloud router id
    id: Optional[str] = _field(default=None)
    # Interconnect OnRamp Google cloud router name
    name: Optional[str] = _field(default=None)
    # Interconnect OnRamp Google cloud router network
    network: Optional[str] = _field(default=None)
    # Interconnect OnRamp Google cloud router region
    region: Optional[str] = _field(default=None)


@dataclass
class ConnectionDetail:
    """
    Interconnect cross connection attachment connection details
    """

    # Interconnect cross connection name
    connection_name: str = _field(metadata={"alias": "connectionName"})


@dataclass
class InterconnectAttachments:
    """
    Interconnect OnRamp gateway connection interconnect attachments
    """

    # Interconnect cross connection attachment resource type
    resource_type: str = _field(metadata={"alias": "resourceType"})
    # Interconnect cross connection attachment connection details
    connection_details: Optional[ConnectionDetail] = _field(
        default=None, metadata={"alias": "connectionDetails"}
    )


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
class VirtualWanDetails:
    """
    Interconnect OnRamp gateway connection Azure virtual wan details
    """

    # Interconnect OnRamp Azure virtual wan cloud resource id
    cloud_resource_id: str = _field(metadata={"alias": "cloudResourceId"})
    # Interconnect OnRamp Azure virtual wan id
    id: Optional[str] = _field(default=None)
    # Interconnect OnRamp Azure virtual wan name
    name: Optional[str] = _field(default=None)
    # Interconnect OnRamp Azure virtual wan resource group
    resource_group_name: Optional[str] = _field(
        default=None, metadata={"alias": "resourceGroupName"}
    )


@dataclass
class InterconnectOnRampGatewayConnection:
    # Interconnect cloud connect cloud access type
    cloud_access_type: str = _field(metadata={"alias": "cloudAccessType"})
    # Interconnect OnRamp gateway connection cloud connect cloud account id
    cloud_account_id: str = _field(metadata={"alias": "cloudAccountId"})
    # Interconnect OnRamp gateway connection cloud connect cloud account id
    cloud_account_name: str = _field(metadata={"alias": "cloudAccountName"})
    # Interconnect OnRamp gateway connection cloud connect cloud provider type
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    # Interconnect OnRamp gateway connection id
    connection_id: str = _field(metadata={"alias": "connectionId"})
    # Interconnect OnRamp gateway connection name
    connection_name: str = _field(metadata={"alias": "connectionName"})
    # Interconnect OnRamp gateway optional description
    description: Optional[str] = _field(default=None)
    # Interconnect OnRamp gateway connection Direct connect gateway details
    direct_connect_gateway_details: Optional[DirectConnectGatewayDetails] = _field(
        default=None, metadata={"alias": "directConnectGatewayDetails"}
    )
    # Interconnect OnRamp gateway connection Express route circuit details
    express_route_circuit_details: Optional[ExpressRouteCircuitDetails] = _field(
        default=None, metadata={"alias": "expressRouteCircuitDetails"}
    )
    # Interconnect OnRamp gateway connection gateway associations
    gateway_associations: Optional[List[GatewayAssociationDetail]] = _field(
        default=None, metadata={"alias": "gatewayAssociations"}
    )
    # Interconnect OnRamp gateway connection Google cloud router details
    google_cloud_router_details: Optional[List[GoogleCloudRouterDetails]] = _field(
        default=None, metadata={"alias": "googleCloudRouterDetails"}
    )
    # Interconnect OnRamp gateway connection interconnect attachments
    interconnect_attachments: Optional[List[InterconnectAttachments]] = _field(
        default=None, metadata={"alias": "interconnectAttachments"}
    )
    # Interconnect virtual network connection resource state information
    interconnect_resource_state: Optional[InterconnectResourceState] = _field(
        default=None, metadata={"alias": "interconnectResourceState"}
    )
    # Interconnect cloud connect cloud access type
    on_ramp_gateway_type: Optional[str] = _field(
        default=None, metadata={"alias": "onRampGatewayType"}
    )
    # Interconnect cloud connect virtual network association type
    virtual_network_association_type: Optional[str] = _field(
        default=None, metadata={"alias": "virtualNetworkAssociationType"}
    )
    # Interconnect OnRamp gateway connection Azure virtual wan details
    virtual_wan_details: Optional[VirtualWanDetails] = _field(
        default=None, metadata={"alias": "virtualWanDetails"}
    )


@dataclass
class CreateInterconnectOnRampGatewayConnectionPostRequest:
    value_type: Optional[ValueType] = _field(default=None, metadata={"alias": "valueType"})


@dataclass
class ProcessResponse:
    # Procees Id of the task
    id: Optional[str] = _field(default=None)


@dataclass
class UpdateInterconnectOnRampGatewayConnectionPutRequest:
    empty: Optional[bool] = _field(default=None)
    value_type: Optional[ValueType] = _field(default=None, metadata={"alias": "valueType"})
