# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class ProcessResponse:
    # Procees Id of the task
    id: Optional[str] = _field(default=None)


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
class OnRampGatewayConnection:
    """
    Interconnect onRamp gateway connection information
    """

    # Interconnect onRamp gateway connection name
    name: str
    # Interconnect onRamp gateway connection id
    id: Optional[str] = _field(default=None)


@dataclass
class VirtualNetworkTagAssociation:
    """
    Interconnect virtual network connection virtual network tag association list
    """

    # Type of resource to be associated to the tag
    resource_type: str = _field(metadata={"alias": "resourceType"})
    # Interconnect onRamp gateway connection information
    on_ramp_gateway_connection: Optional[OnRampGatewayConnection] = _field(
        default=None, metadata={"alias": "onRampGatewayConnection"}
    )


@dataclass
class VirtualNetworkTag:
    """
    Interconnect virtual network connection virtual network tag list
    """

    # Name of the Host VPC/VNET tag
    tag_name: str = _field(metadata={"alias": "tagName"})


@dataclass
class InterconnectVirtualNetworkConnection:
    # Interconnect virtual network connection cloud account id
    cloud_account_id: str = _field(metadata={"alias": "cloudAccountId"})
    # Interconnect virtual network connection cloud account name
    cloud_account_name: str = _field(metadata={"alias": "cloudAccountName"})
    # Cloud provider type
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    # Interconnect  virtual network connection name
    connection_name: str = _field(metadata={"alias": "connectionName"})
    # Interconnect virtual network connection tag association type
    virtual_network_tag_association_type: str = _field(
        metadata={"alias": "virtualNetworkTagAssociationType"}
    )
    # Interconnect virtual network connection virtual network tag association list
    virtual_network_tag_associations: List[VirtualNetworkTagAssociation] = _field(
        metadata={"alias": "virtualNetworkTagAssociations"}
    )
    # Interconnect virtual network connection virtual network tag list
    virtual_network_tags: List[VirtualNetworkTag] = _field(metadata={"alias": "virtualNetworkTags"})
    # Interconnect virtual network connection id
    connection_id: Optional[str] = _field(default=None, metadata={"alias": "connectionId"})
    # Interconnect virtual network connection resource state information
    resource_state: Optional[InterconnectResourceState] = _field(
        default=None, metadata={"alias": "resourceState"}
    )
