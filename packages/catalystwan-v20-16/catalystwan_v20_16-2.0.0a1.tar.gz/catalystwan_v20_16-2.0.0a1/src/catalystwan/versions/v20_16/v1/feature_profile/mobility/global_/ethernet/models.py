# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

Type = Literal[
    "cellular", "ethernet", "globalSettings", "networkProtocol", "securityPolicy", "wifi"
]


@dataclass
class Variable:
    json_path: str = _field(metadata={"alias": "jsonPath"})
    var_name: str = _field(metadata={"alias": "varName"})


@dataclass
class AaaServerInfo:
    aaa_servers_parcel_id: str = _field(metadata={"alias": "aaaServersParcelId"})
    radius_server_name: str = _field(metadata={"alias": "radiusServerName"})


@dataclass
class EthernetInterface:
    interface_name: str = _field(metadata={"alias": "interfaceName"})
    port_type: str = _field(metadata={"alias": "portType"})
    aaa_server_info: Optional[AaaServerInfo] = _field(
        default=None, metadata={"alias": "aaaServerInfo"}
    )
    admin_state: Optional[str] = _field(default=None, metadata={"alias": "adminState"})
    corporate_lan: Optional[bool] = _field(default=None, metadata={"alias": "corporateLan"})
    ip_assignment: Optional[str] = _field(default=None, metadata={"alias": "ipAssignment"})
    ipv6_assignment: Optional[str] = _field(default=None, metadata={"alias": "ipv6Assignment"})
    static_ip_address: Optional[str] = _field(default=None, metadata={"alias": "staticIpAddress"})
    static_ip_address_subnet_mask: Optional[str] = _field(
        default=None, metadata={"alias": "staticIpAddressSubnetMask"}
    )
    static_route_ip: Optional[str] = _field(default=None, metadata={"alias": "staticRouteIp"})
    wan_configuration: Optional[str] = _field(default=None, metadata={"alias": "wanConfiguration"})


@dataclass
class Ethernet:
    ethernet_interface_list: List[EthernetInterface] = _field(
        metadata={"alias": "ethernetInterfaceList"}
    )
    # Name of the Profile Parcel. Must be unique.
    name: str
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    variables: Optional[List[Variable]] = _field(default=None)


@dataclass
class Data:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    payload: Optional[Ethernet] = _field(default=None)


@dataclass
class GetListMobilityGlobalEthernetPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateEthernetProfileParcelForMobilityPostRequest:
    ethernet_interface_list: List[EthernetInterface] = _field(
        metadata={"alias": "ethernetInterfaceList"}
    )
    # Name of the Profile Parcel. Must be unique.
    name: str
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    variables: Optional[List[Variable]] = _field(default=None)


@dataclass
class GetEthernetProfileParcelGetResponse:
    ethernet_interface_list: List[EthernetInterface] = _field(
        metadata={"alias": "ethernetInterfaceList"}
    )
    # Name of the Profile Parcel. Must be unique.
    name: str
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    variables: Optional[List[Variable]] = _field(default=None)


@dataclass
class EditEthernetProfileParcelForSystemPutRequest:
    ethernet_interface_list: List[EthernetInterface] = _field(
        metadata={"alias": "ethernetInterfaceList"}
    )
    # Name of the Profile Parcel. Must be unique.
    name: str
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    variables: Optional[List[Variable]] = _field(default=None)
