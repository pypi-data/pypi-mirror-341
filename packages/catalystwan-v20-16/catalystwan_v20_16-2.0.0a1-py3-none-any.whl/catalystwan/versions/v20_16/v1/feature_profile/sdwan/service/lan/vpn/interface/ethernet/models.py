# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class Payload:
    """
    LAN VPN Interface Ethernet profile parcel schema for POST request
    """

    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


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
    # LAN VPN Interface Ethernet profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanServiceLanVpnInterfaceEthernetPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateLanVpnInterfaceEthernetParcelForServicePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateLanVpnInterfaceEthernetParcelForServicePostRequest:
    """
    LAN VPN Interface Ethernet profile parcel schema for POST request
    """

    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EthernetPayload:
    """
    LAN VPN Interface Ethernet profile parcel schema for PUT request
    """

    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanServiceLanVpnInterfaceEthernetPayload:
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
    # LAN VPN Interface Ethernet profile parcel schema for PUT request
    payload: Optional[EthernetPayload] = _field(default=None)


@dataclass
class EditLanVpnInterfaceEthernetParcelForServicePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditLanVpnInterfaceEthernetParcelForServicePutRequest:
    """
    LAN VPN Interface Ethernet profile parcel schema for PUT request
    """

    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
