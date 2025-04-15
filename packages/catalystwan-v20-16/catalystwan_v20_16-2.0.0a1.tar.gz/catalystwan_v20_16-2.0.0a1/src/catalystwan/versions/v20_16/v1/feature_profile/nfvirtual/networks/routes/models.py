# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]


@dataclass
class CreateNfvirtualRoutesParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfRoutesNetworkAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRoutesNetworkAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRoutesNexthopAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfRoutesNexthopAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Routes:
    network_address: Optional[
        Union[OneOfRoutesNetworkAddressOptionsDef1, OneOfRoutesNetworkAddressOptionsDef2]
    ] = _field(default=None)
    nexthop_address: Optional[
        Union[OneOfRoutesNexthopAddressOptionsDef1, OneOfRoutesNexthopAddressOptionsDef2]
    ] = _field(default=None)


@dataclass
class Data:
    # List of Routes
    routes: Optional[List[Routes]] = _field(default=None)


@dataclass
class CreateNfvirtualRoutesParcelPostRequest:
    """
    Routes profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class RoutesOneOfRoutesNetworkAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RoutesOneOfRoutesNexthopAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class RoutesRoutes:
    network_address: Optional[
        Union[RoutesOneOfRoutesNetworkAddressOptionsDef1, OneOfRoutesNetworkAddressOptionsDef2]
    ] = _field(default=None)
    nexthop_address: Optional[
        Union[RoutesOneOfRoutesNexthopAddressOptionsDef1, OneOfRoutesNexthopAddressOptionsDef2]
    ] = _field(default=None)


@dataclass
class RoutesData:
    # List of Routes
    routes: Optional[List[RoutesRoutes]] = _field(default=None)


@dataclass
class Payload:
    """
    Routes profile parcel schema for PUT request
    """

    data: RoutesData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualNetworksRoutesPayload:
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
    # Routes profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditNfvirtualRoutesParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class NetworksRoutesOneOfRoutesNetworkAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksRoutesOneOfRoutesNexthopAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class NetworksRoutesRoutes:
    network_address: Optional[
        Union[
            NetworksRoutesOneOfRoutesNetworkAddressOptionsDef1, OneOfRoutesNetworkAddressOptionsDef2
        ]
    ] = _field(default=None)
    nexthop_address: Optional[
        Union[
            NetworksRoutesOneOfRoutesNexthopAddressOptionsDef1, OneOfRoutesNexthopAddressOptionsDef2
        ]
    ] = _field(default=None)


@dataclass
class NetworksRoutesData:
    # List of Routes
    routes: Optional[List[NetworksRoutesRoutes]] = _field(default=None)


@dataclass
class EditNfvirtualRoutesParcelPutRequest:
    """
    Routes profile parcel schema for PUT request
    """

    data: NetworksRoutesData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
