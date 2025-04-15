# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

EndpointTrackerTypeDef = Literal["ipv6-interface", "ipv6-interface-icmp"]

DefaultEndpointTrackerTypeDef = Literal["ipv6-interface"]

TrackerTypeDef = Literal["endpoint"]

DefaultTrackerTypeDef = Literal["endpoint"]

Ipv6TrackerEndpointTrackerTypeDef = Literal["ipv6-interface", "ipv6-interface-icmp"]

Ipv6TrackerDefaultEndpointTrackerTypeDef = Literal["ipv6-interface"]

Ipv6TrackerTrackerTypeDef = Literal["endpoint"]

Ipv6TrackerDefaultTrackerTypeDef = Literal["endpoint"]

TransportIpv6TrackerEndpointTrackerTypeDef = Literal["ipv6-interface", "ipv6-interface-icmp"]

TransportIpv6TrackerDefaultEndpointTrackerTypeDef = Literal["ipv6-interface"]

TransportIpv6TrackerTrackerTypeDef = Literal["endpoint"]

TransportIpv6TrackerDefaultTrackerTypeDef = Literal["endpoint"]


@dataclass
class OneOfTrackerNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEndpointApiUrlOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEndpointApiUrlOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEndpointDnsNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEndpointDnsNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEndpointIpOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEndpointIpOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIntervalOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIcmpIntervalOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIcmpIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIcmpIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMultiplierOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMultiplierOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMultiplierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfThresholdOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfThresholdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEndpointTrackerTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EndpointTrackerTypeDef


@dataclass
class OneOfEndpointTrackerTypeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultEndpointTrackerTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTrackerTypeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TrackerTypeDef


@dataclass
class OneOfTrackerTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultTrackerTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Ipv6TrackerData:
    endpoint_api_url: Optional[
        Union[OneOfEndpointApiUrlOptionsDef1, OneOfEndpointApiUrlOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointApiUrl"})
    endpoint_dns_name: Optional[
        Union[OneOfEndpointDnsNameOptionsDef1, OneOfEndpointDnsNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointDnsName"})
    endpoint_ip: Optional[Union[OneOfEndpointIpOptionsDef1, OneOfEndpointIpOptionsDef2]] = _field(
        default=None, metadata={"alias": "endpointIp"}
    )
    endpoint_tracker_type: Optional[
        Union[OneOfEndpointTrackerTypeOptionsDef1, OneOfEndpointTrackerTypeOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointTrackerType"})
    icmp_interval: Optional[
        Union[
            OneOfIcmpIntervalOptionsDef1, OneOfIcmpIntervalOptionsDef2, OneOfIcmpIntervalOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "icmpInterval"})
    interval: Optional[
        Union[OneOfIntervalOptionsDef1, OneOfIntervalOptionsDef2, OneOfIntervalOptionsDef3]
    ] = _field(default=None)
    multiplier: Optional[
        Union[OneOfMultiplierOptionsDef1, OneOfMultiplierOptionsDef2, OneOfMultiplierOptionsDef3]
    ] = _field(default=None)
    threshold: Optional[
        Union[OneOfThresholdOptionsDef1, OneOfThresholdOptionsDef2, OneOfThresholdOptionsDef3]
    ] = _field(default=None)
    tracker_name: Optional[Union[OneOfTrackerNameOptionsDef1, OneOfTrackerNameOptionsDef2]] = (
        _field(default=None, metadata={"alias": "trackerName"})
    )
    tracker_type: Optional[
        Union[OneOfTrackerTypeOptionsDef1, OneOfTrackerTypeOptionsDef2, OneOfTrackerTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "trackerType"})


@dataclass
class Payload:
    """
    IPv6 Tracker profile parcel schema for POST request
    """

    data: Ipv6TrackerData
    name: str
    # Set the parcel description
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
    # IPv6 Tracker profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportIpv6TrackerPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateIpv6TrackerProfileParcelForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportIpv6TrackerData:
    endpoint_api_url: Optional[
        Union[OneOfEndpointApiUrlOptionsDef1, OneOfEndpointApiUrlOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointApiUrl"})
    endpoint_dns_name: Optional[
        Union[OneOfEndpointDnsNameOptionsDef1, OneOfEndpointDnsNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointDnsName"})
    endpoint_ip: Optional[Union[OneOfEndpointIpOptionsDef1, OneOfEndpointIpOptionsDef2]] = _field(
        default=None, metadata={"alias": "endpointIp"}
    )
    endpoint_tracker_type: Optional[
        Union[OneOfEndpointTrackerTypeOptionsDef1, OneOfEndpointTrackerTypeOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointTrackerType"})
    icmp_interval: Optional[
        Union[
            OneOfIcmpIntervalOptionsDef1, OneOfIcmpIntervalOptionsDef2, OneOfIcmpIntervalOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "icmpInterval"})
    interval: Optional[
        Union[OneOfIntervalOptionsDef1, OneOfIntervalOptionsDef2, OneOfIntervalOptionsDef3]
    ] = _field(default=None)
    multiplier: Optional[
        Union[OneOfMultiplierOptionsDef1, OneOfMultiplierOptionsDef2, OneOfMultiplierOptionsDef3]
    ] = _field(default=None)
    threshold: Optional[
        Union[OneOfThresholdOptionsDef1, OneOfThresholdOptionsDef2, OneOfThresholdOptionsDef3]
    ] = _field(default=None)
    tracker_name: Optional[Union[OneOfTrackerNameOptionsDef1, OneOfTrackerNameOptionsDef2]] = (
        _field(default=None, metadata={"alias": "trackerName"})
    )
    tracker_type: Optional[
        Union[OneOfTrackerTypeOptionsDef1, OneOfTrackerTypeOptionsDef2, OneOfTrackerTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "trackerType"})


@dataclass
class CreateIpv6TrackerProfileParcelForTransportPostRequest:
    """
    IPv6 Tracker profile parcel schema for POST request
    """

    data: TransportIpv6TrackerData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Ipv6TrackerOneOfTrackerNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Ipv6TrackerOneOfEndpointApiUrlOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Ipv6TrackerOneOfEndpointDnsNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Ipv6TrackerOneOfEndpointIpOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Ipv6TrackerOneOfIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Ipv6TrackerOneOfIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Ipv6TrackerOneOfIcmpIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Ipv6TrackerOneOfIcmpIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Ipv6TrackerOneOfMultiplierOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Ipv6TrackerOneOfMultiplierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Ipv6TrackerOneOfThresholdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Ipv6TrackerOneOfThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Ipv6TrackerOneOfEndpointTrackerTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv6TrackerEndpointTrackerTypeDef


@dataclass
class Ipv6TrackerOneOfEndpointTrackerTypeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv6TrackerDefaultEndpointTrackerTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Ipv6TrackerOneOfTrackerTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv6TrackerTrackerTypeDef


@dataclass
class Ipv6TrackerOneOfTrackerTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv6TrackerDefaultTrackerTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanTransportIpv6TrackerData:
    endpoint_api_url: Optional[
        Union[OneOfEndpointApiUrlOptionsDef1, Ipv6TrackerOneOfEndpointApiUrlOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointApiUrl"})
    endpoint_dns_name: Optional[
        Union[OneOfEndpointDnsNameOptionsDef1, Ipv6TrackerOneOfEndpointDnsNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointDnsName"})
    endpoint_ip: Optional[
        Union[OneOfEndpointIpOptionsDef1, Ipv6TrackerOneOfEndpointIpOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointIp"})
    endpoint_tracker_type: Optional[
        Union[
            Ipv6TrackerOneOfEndpointTrackerTypeOptionsDef1,
            Ipv6TrackerOneOfEndpointTrackerTypeOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "endpointTrackerType"})
    icmp_interval: Optional[
        Union[
            OneOfIcmpIntervalOptionsDef1,
            Ipv6TrackerOneOfIcmpIntervalOptionsDef2,
            Ipv6TrackerOneOfIcmpIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpInterval"})
    interval: Optional[
        Union[
            OneOfIntervalOptionsDef1,
            Ipv6TrackerOneOfIntervalOptionsDef2,
            Ipv6TrackerOneOfIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    multiplier: Optional[
        Union[
            OneOfMultiplierOptionsDef1,
            Ipv6TrackerOneOfMultiplierOptionsDef2,
            Ipv6TrackerOneOfMultiplierOptionsDef3,
        ]
    ] = _field(default=None)
    threshold: Optional[
        Union[
            OneOfThresholdOptionsDef1,
            Ipv6TrackerOneOfThresholdOptionsDef2,
            Ipv6TrackerOneOfThresholdOptionsDef3,
        ]
    ] = _field(default=None)
    tracker_name: Optional[
        Union[OneOfTrackerNameOptionsDef1, Ipv6TrackerOneOfTrackerNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "trackerName"})
    tracker_type: Optional[
        Union[
            OneOfTrackerTypeOptionsDef1,
            Ipv6TrackerOneOfTrackerTypeOptionsDef2,
            Ipv6TrackerOneOfTrackerTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackerType"})


@dataclass
class Ipv6TrackerPayload:
    """
    IPv6 Tracker profile parcel schema for PUT request
    """

    data: SdwanTransportIpv6TrackerData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanTransportIpv6TrackerPayload:
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
    # IPv6 Tracker profile parcel schema for PUT request
    payload: Optional[Ipv6TrackerPayload] = _field(default=None)


@dataclass
class EditIpv6TrackerProfileParcelForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportIpv6TrackerOneOfTrackerNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportIpv6TrackerOneOfEndpointApiUrlOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportIpv6TrackerOneOfEndpointDnsNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportIpv6TrackerOneOfEndpointIpOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportIpv6TrackerOneOfIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportIpv6TrackerOneOfIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportIpv6TrackerOneOfIcmpIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportIpv6TrackerOneOfIcmpIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportIpv6TrackerOneOfMultiplierOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportIpv6TrackerOneOfMultiplierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportIpv6TrackerOneOfThresholdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportIpv6TrackerOneOfThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportIpv6TrackerOneOfEndpointTrackerTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportIpv6TrackerEndpointTrackerTypeDef


@dataclass
class TransportIpv6TrackerOneOfEndpointTrackerTypeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportIpv6TrackerDefaultEndpointTrackerTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class TransportIpv6TrackerOneOfTrackerTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportIpv6TrackerTrackerTypeDef


@dataclass
class TransportIpv6TrackerOneOfTrackerTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportIpv6TrackerDefaultTrackerTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdwanTransportIpv6TrackerData:
    endpoint_api_url: Optional[
        Union[OneOfEndpointApiUrlOptionsDef1, TransportIpv6TrackerOneOfEndpointApiUrlOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointApiUrl"})
    endpoint_dns_name: Optional[
        Union[OneOfEndpointDnsNameOptionsDef1, TransportIpv6TrackerOneOfEndpointDnsNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointDnsName"})
    endpoint_ip: Optional[
        Union[OneOfEndpointIpOptionsDef1, TransportIpv6TrackerOneOfEndpointIpOptionsDef2]
    ] = _field(default=None, metadata={"alias": "endpointIp"})
    endpoint_tracker_type: Optional[
        Union[
            TransportIpv6TrackerOneOfEndpointTrackerTypeOptionsDef1,
            TransportIpv6TrackerOneOfEndpointTrackerTypeOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "endpointTrackerType"})
    icmp_interval: Optional[
        Union[
            OneOfIcmpIntervalOptionsDef1,
            TransportIpv6TrackerOneOfIcmpIntervalOptionsDef2,
            TransportIpv6TrackerOneOfIcmpIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpInterval"})
    interval: Optional[
        Union[
            OneOfIntervalOptionsDef1,
            TransportIpv6TrackerOneOfIntervalOptionsDef2,
            TransportIpv6TrackerOneOfIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    multiplier: Optional[
        Union[
            OneOfMultiplierOptionsDef1,
            TransportIpv6TrackerOneOfMultiplierOptionsDef2,
            TransportIpv6TrackerOneOfMultiplierOptionsDef3,
        ]
    ] = _field(default=None)
    threshold: Optional[
        Union[
            OneOfThresholdOptionsDef1,
            TransportIpv6TrackerOneOfThresholdOptionsDef2,
            TransportIpv6TrackerOneOfThresholdOptionsDef3,
        ]
    ] = _field(default=None)
    tracker_name: Optional[
        Union[OneOfTrackerNameOptionsDef1, TransportIpv6TrackerOneOfTrackerNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "trackerName"})
    tracker_type: Optional[
        Union[
            OneOfTrackerTypeOptionsDef1,
            TransportIpv6TrackerOneOfTrackerTypeOptionsDef2,
            TransportIpv6TrackerOneOfTrackerTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackerType"})


@dataclass
class EditIpv6TrackerProfileParcelForTransportPutRequest:
    """
    IPv6 Tracker profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanTransportIpv6TrackerData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
