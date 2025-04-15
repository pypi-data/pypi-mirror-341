# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

TransportGatewayEnumDef = Literal["ecmp-with-direct-path", "prefer"]

SiteTypeListDef = Literal["br", "branch", "cloud", "spoke", "type-1", "type-2", "type-3"]

OmpTransportGatewayEnumDef = Literal["ecmp-with-direct-path", "prefer"]

OmpSiteTypeListDef = Literal["br", "branch", "cloud", "spoke", "type-1", "type-2", "type-3"]

SystemOmpSiteTypeListDef = Literal["br", "branch", "cloud", "spoke", "type-1", "type-2", "type-3"]

SystemOmpTransportGatewayEnumDef = Literal["ecmp-with-direct-path", "prefer"]

SdwanSystemOmpSiteTypeListDef = Literal[
    "br", "branch", "cloud", "spoke", "type-1", "type-2", "type-3"
]

FeatureProfileSdwanSystemOmpSiteTypeListDef = Literal[
    "br", "branch", "cloud", "spoke", "type-1", "type-2", "type-3"
]


@dataclass
class OneOfGracefulRestartOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfGracefulRestartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfGracefulRestartOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOverlayAsOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOverlayAsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOverlayAsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSendPathLimitOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSendPathLimitOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSendPathLimitOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEcmpLimitOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEcmpLimitOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEcmpLimitOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShutdownOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfShutdownOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfShutdownOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOmpAdminDistanceIpv4OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOmpAdminDistanceIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOmpAdminDistanceIpv4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfOmpAdminDistanceIpv6OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOmpAdminDistanceIpv6OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOmpAdminDistanceIpv6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfAdvertisementIntervalOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAdvertisementIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAdvertisementIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfGracefulRestartTimerOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfGracefulRestartTimerOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfGracefulRestartTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEorTimerOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEorTimerOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEorTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHoldtimeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAdvertiseProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAdvertiseProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAdvertiseProtocolOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAdvertiseConnectedOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAdvertiseConnectedOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAdvertiseConnectedOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # use enum for backward compatibility, use default for UI to display default value
    value: Optional[bool] = _field(default=True)


@dataclass
class OneOfAdvertiseStaticOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAdvertiseStaticOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAdvertiseStaticOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # use enum for backward compatibility, use default for UI to display default value
    value: Optional[bool] = _field(default=True)


@dataclass
class AdvertiseIpv4:
    bgp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    connected: Union[
        OneOfAdvertiseConnectedOptionsDef1,
        OneOfAdvertiseConnectedOptionsDef2,
        OneOfAdvertiseConnectedOptionsDef3,
    ]
    eigrp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    isis: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    lisp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    ospf: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    ospfv3: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    static: Union[
        OneOfAdvertiseStaticOptionsDef1,
        OneOfAdvertiseStaticOptionsDef2,
        OneOfAdvertiseStaticOptionsDef3,
    ]


@dataclass
class AdvertiseIpv6:
    bgp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    connected: Union[
        OneOfAdvertiseConnectedOptionsDef1,
        OneOfAdvertiseConnectedOptionsDef2,
        OneOfAdvertiseConnectedOptionsDef3,
    ]
    eigrp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    isis: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    lisp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    ospf: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    static: Union[
        OneOfAdvertiseStaticOptionsDef1,
        OneOfAdvertiseStaticOptionsDef2,
        OneOfAdvertiseStaticOptionsDef3,
    ]


@dataclass
class OneOfIgnoreRegionPathLengthOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIgnoreRegionPathLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIgnoreRegionPathLengthOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTransportGatewayOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTransportGatewayOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportGatewayEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTransportGatewayOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSiteTypesOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSiteTypesOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[SiteTypeListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSiteTypesOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OmpData:
    advertise_ipv4: AdvertiseIpv4 = _field(metadata={"alias": "advertiseIpv4"})
    advertise_ipv6: AdvertiseIpv6 = _field(metadata={"alias": "advertiseIpv6"})
    advertisement_interval: Union[
        OneOfAdvertisementIntervalOptionsDef1,
        OneOfAdvertisementIntervalOptionsDef2,
        OneOfAdvertisementIntervalOptionsDef3,
    ] = _field(metadata={"alias": "advertisementInterval"})
    ecmp_limit: Union[
        OneOfEcmpLimitOptionsDef1, OneOfEcmpLimitOptionsDef2, OneOfEcmpLimitOptionsDef3
    ] = _field(metadata={"alias": "ecmpLimit"})
    eor_timer: Union[
        OneOfEorTimerOptionsDef1, OneOfEorTimerOptionsDef2, OneOfEorTimerOptionsDef3
    ] = _field(metadata={"alias": "eorTimer"})
    graceful_restart: Union[
        OneOfGracefulRestartOptionsDef1,
        OneOfGracefulRestartOptionsDef2,
        OneOfGracefulRestartOptionsDef3,
    ] = _field(metadata={"alias": "gracefulRestart"})
    graceful_restart_timer: Union[
        OneOfGracefulRestartTimerOptionsDef1,
        OneOfGracefulRestartTimerOptionsDef2,
        OneOfGracefulRestartTimerOptionsDef3,
    ] = _field(metadata={"alias": "gracefulRestartTimer"})
    holdtime: Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3]
    omp_admin_distance_ipv4: Union[
        OneOfOmpAdminDistanceIpv4OptionsDef1,
        OneOfOmpAdminDistanceIpv4OptionsDef2,
        OneOfOmpAdminDistanceIpv4OptionsDef3,
    ] = _field(metadata={"alias": "ompAdminDistanceIpv4"})
    omp_admin_distance_ipv6: Union[
        OneOfOmpAdminDistanceIpv6OptionsDef1,
        OneOfOmpAdminDistanceIpv6OptionsDef2,
        OneOfOmpAdminDistanceIpv6OptionsDef3,
    ] = _field(metadata={"alias": "ompAdminDistanceIpv6"})
    overlay_as: Union[
        OneOfOverlayAsOptionsDef1, OneOfOverlayAsOptionsDef2, OneOfOverlayAsOptionsDef3
    ] = _field(metadata={"alias": "overlayAs"})
    send_path_limit: Union[
        OneOfSendPathLimitOptionsDef1, OneOfSendPathLimitOptionsDef2, OneOfSendPathLimitOptionsDef3
    ] = _field(metadata={"alias": "sendPathLimit"})
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    aspath_auto_translation: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "aspathAutoTranslation"})
    ignore_region_path_length: Optional[
        Union[
            OneOfIgnoreRegionPathLengthOptionsDef1,
            OneOfIgnoreRegionPathLengthOptionsDef2,
            OneOfIgnoreRegionPathLengthOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ignoreRegionPathLength"})
    site_types: Optional[
        Union[OneOfSiteTypesOptionsDef1, OneOfSiteTypesOptionsDef2, OneOfSiteTypesOptionsDef3]
    ] = _field(default=None, metadata={"alias": "siteTypes"})
    site_types_for_transport_gateway: Optional[
        Union[OneOfSiteTypesOptionsDef1, OneOfSiteTypesOptionsDef2, OneOfSiteTypesOptionsDef3]
    ] = _field(default=None, metadata={"alias": "siteTypesForTransportGateway"})
    transport_gateway: Optional[
        Union[
            OneOfTransportGatewayOptionsDef1,
            OneOfTransportGatewayOptionsDef2,
            OneOfTransportGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "transportGateway"})


@dataclass
class Payload:
    """
    OMP profile parcel schema for POST request
    """

    data: OmpData
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
    # OMP profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSystemOmpPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateOmpProfileParcelForSystemPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemOmpData:
    advertise_ipv4: AdvertiseIpv4 = _field(metadata={"alias": "advertiseIpv4"})
    advertise_ipv6: AdvertiseIpv6 = _field(metadata={"alias": "advertiseIpv6"})
    advertisement_interval: Union[
        OneOfAdvertisementIntervalOptionsDef1,
        OneOfAdvertisementIntervalOptionsDef2,
        OneOfAdvertisementIntervalOptionsDef3,
    ] = _field(metadata={"alias": "advertisementInterval"})
    ecmp_limit: Union[
        OneOfEcmpLimitOptionsDef1, OneOfEcmpLimitOptionsDef2, OneOfEcmpLimitOptionsDef3
    ] = _field(metadata={"alias": "ecmpLimit"})
    eor_timer: Union[
        OneOfEorTimerOptionsDef1, OneOfEorTimerOptionsDef2, OneOfEorTimerOptionsDef3
    ] = _field(metadata={"alias": "eorTimer"})
    graceful_restart: Union[
        OneOfGracefulRestartOptionsDef1,
        OneOfGracefulRestartOptionsDef2,
        OneOfGracefulRestartOptionsDef3,
    ] = _field(metadata={"alias": "gracefulRestart"})
    graceful_restart_timer: Union[
        OneOfGracefulRestartTimerOptionsDef1,
        OneOfGracefulRestartTimerOptionsDef2,
        OneOfGracefulRestartTimerOptionsDef3,
    ] = _field(metadata={"alias": "gracefulRestartTimer"})
    holdtime: Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3]
    omp_admin_distance_ipv4: Union[
        OneOfOmpAdminDistanceIpv4OptionsDef1,
        OneOfOmpAdminDistanceIpv4OptionsDef2,
        OneOfOmpAdminDistanceIpv4OptionsDef3,
    ] = _field(metadata={"alias": "ompAdminDistanceIpv4"})
    omp_admin_distance_ipv6: Union[
        OneOfOmpAdminDistanceIpv6OptionsDef1,
        OneOfOmpAdminDistanceIpv6OptionsDef2,
        OneOfOmpAdminDistanceIpv6OptionsDef3,
    ] = _field(metadata={"alias": "ompAdminDistanceIpv6"})
    overlay_as: Union[
        OneOfOverlayAsOptionsDef1, OneOfOverlayAsOptionsDef2, OneOfOverlayAsOptionsDef3
    ] = _field(metadata={"alias": "overlayAs"})
    send_path_limit: Union[
        OneOfSendPathLimitOptionsDef1, OneOfSendPathLimitOptionsDef2, OneOfSendPathLimitOptionsDef3
    ] = _field(metadata={"alias": "sendPathLimit"})
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    aspath_auto_translation: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "aspathAutoTranslation"})
    ignore_region_path_length: Optional[
        Union[
            OneOfIgnoreRegionPathLengthOptionsDef1,
            OneOfIgnoreRegionPathLengthOptionsDef2,
            OneOfIgnoreRegionPathLengthOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ignoreRegionPathLength"})
    site_types: Optional[
        Union[OneOfSiteTypesOptionsDef1, OneOfSiteTypesOptionsDef2, OneOfSiteTypesOptionsDef3]
    ] = _field(default=None, metadata={"alias": "siteTypes"})
    site_types_for_transport_gateway: Optional[
        Union[OneOfSiteTypesOptionsDef1, OneOfSiteTypesOptionsDef2, OneOfSiteTypesOptionsDef3]
    ] = _field(default=None, metadata={"alias": "siteTypesForTransportGateway"})
    transport_gateway: Optional[
        Union[
            OneOfTransportGatewayOptionsDef1,
            OneOfTransportGatewayOptionsDef2,
            OneOfTransportGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "transportGateway"})


@dataclass
class CreateOmpProfileParcelForSystemPostRequest:
    """
    OMP profile parcel schema for POST request
    """

    data: SystemOmpData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OmpOneOfOverlayAsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OmpOneOfSendPathLimitOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OmpOneOfEcmpLimitOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OmpOneOfOmpAdminDistanceIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OmpOneOfOmpAdminDistanceIpv4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[int] = _field(default=251)


@dataclass
class OmpOneOfOmpAdminDistanceIpv6OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OmpOneOfOmpAdminDistanceIpv6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[int] = _field(default=251)


@dataclass
class OmpOneOfAdvertisementIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OmpOneOfGracefulRestartTimerOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OmpOneOfEorTimerOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OmpOneOfHoldtimeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OmpOneOfAdvertiseConnectedOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # use enum for backward compatibility, use default for UI to display default value
    value: Optional[bool] = _field(default=True)


@dataclass
class OmpOneOfAdvertiseStaticOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # use enum for backward compatibility, use default for UI to display default value
    value: Optional[bool] = _field(default=True)


@dataclass
class OmpAdvertiseIpv4:
    bgp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    connected: Union[
        OneOfAdvertiseConnectedOptionsDef1,
        OneOfAdvertiseConnectedOptionsDef2,
        OmpOneOfAdvertiseConnectedOptionsDef3,
    ]
    eigrp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    isis: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    lisp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    ospf: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    ospfv3: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    static: Union[
        OneOfAdvertiseStaticOptionsDef1,
        OneOfAdvertiseStaticOptionsDef2,
        OmpOneOfAdvertiseStaticOptionsDef3,
    ]


@dataclass
class SystemOmpOneOfAdvertiseConnectedOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # use enum for backward compatibility, use default for UI to display default value
    value: Optional[bool] = _field(default=True)


@dataclass
class SystemOmpOneOfAdvertiseStaticOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # use enum for backward compatibility, use default for UI to display default value
    value: Optional[bool] = _field(default=True)


@dataclass
class OmpAdvertiseIpv6:
    bgp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    connected: Union[
        OneOfAdvertiseConnectedOptionsDef1,
        OneOfAdvertiseConnectedOptionsDef2,
        SystemOmpOneOfAdvertiseConnectedOptionsDef3,
    ]
    eigrp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    isis: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    lisp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    ospf: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    static: Union[
        OneOfAdvertiseStaticOptionsDef1,
        OneOfAdvertiseStaticOptionsDef2,
        SystemOmpOneOfAdvertiseStaticOptionsDef3,
    ]


@dataclass
class OmpOneOfTransportGatewayOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: OmpTransportGatewayEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OmpOneOfSiteTypesOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[OmpSiteTypeListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemOmpOneOfSiteTypesOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[SystemOmpSiteTypeListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanSystemOmpData:
    advertise_ipv4: OmpAdvertiseIpv4 = _field(metadata={"alias": "advertiseIpv4"})
    advertise_ipv6: OmpAdvertiseIpv6 = _field(metadata={"alias": "advertiseIpv6"})
    advertisement_interval: Union[
        OneOfAdvertisementIntervalOptionsDef1,
        OmpOneOfAdvertisementIntervalOptionsDef2,
        OneOfAdvertisementIntervalOptionsDef3,
    ] = _field(metadata={"alias": "advertisementInterval"})
    ecmp_limit: Union[
        OneOfEcmpLimitOptionsDef1, OmpOneOfEcmpLimitOptionsDef2, OneOfEcmpLimitOptionsDef3
    ] = _field(metadata={"alias": "ecmpLimit"})
    eor_timer: Union[
        OneOfEorTimerOptionsDef1, OmpOneOfEorTimerOptionsDef2, OneOfEorTimerOptionsDef3
    ] = _field(metadata={"alias": "eorTimer"})
    graceful_restart: Union[
        OneOfGracefulRestartOptionsDef1,
        OneOfGracefulRestartOptionsDef2,
        OneOfGracefulRestartOptionsDef3,
    ] = _field(metadata={"alias": "gracefulRestart"})
    graceful_restart_timer: Union[
        OneOfGracefulRestartTimerOptionsDef1,
        OmpOneOfGracefulRestartTimerOptionsDef2,
        OneOfGracefulRestartTimerOptionsDef3,
    ] = _field(metadata={"alias": "gracefulRestartTimer"})
    holdtime: Union[OneOfHoldtimeOptionsDef1, OmpOneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3]
    omp_admin_distance_ipv4: Union[
        OneOfOmpAdminDistanceIpv4OptionsDef1,
        OmpOneOfOmpAdminDistanceIpv4OptionsDef2,
        OmpOneOfOmpAdminDistanceIpv4OptionsDef3,
    ] = _field(metadata={"alias": "ompAdminDistanceIpv4"})
    omp_admin_distance_ipv6: Union[
        OneOfOmpAdminDistanceIpv6OptionsDef1,
        OmpOneOfOmpAdminDistanceIpv6OptionsDef2,
        OmpOneOfOmpAdminDistanceIpv6OptionsDef3,
    ] = _field(metadata={"alias": "ompAdminDistanceIpv6"})
    overlay_as: Union[
        OneOfOverlayAsOptionsDef1, OmpOneOfOverlayAsOptionsDef2, OneOfOverlayAsOptionsDef3
    ] = _field(metadata={"alias": "overlayAs"})
    send_path_limit: Union[
        OneOfSendPathLimitOptionsDef1,
        OmpOneOfSendPathLimitOptionsDef2,
        OneOfSendPathLimitOptionsDef3,
    ] = _field(metadata={"alias": "sendPathLimit"})
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    aspath_auto_translation: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "aspathAutoTranslation"})
    ignore_region_path_length: Optional[
        Union[
            OneOfIgnoreRegionPathLengthOptionsDef1,
            OneOfIgnoreRegionPathLengthOptionsDef2,
            OneOfIgnoreRegionPathLengthOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ignoreRegionPathLength"})
    site_types: Optional[
        Union[
            OneOfSiteTypesOptionsDef1, SystemOmpOneOfSiteTypesOptionsDef2, OneOfSiteTypesOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "siteTypes"})
    site_types_for_transport_gateway: Optional[
        Union[OneOfSiteTypesOptionsDef1, OmpOneOfSiteTypesOptionsDef2, OneOfSiteTypesOptionsDef3]
    ] = _field(default=None, metadata={"alias": "siteTypesForTransportGateway"})
    transport_gateway: Optional[
        Union[
            OneOfTransportGatewayOptionsDef1,
            OmpOneOfTransportGatewayOptionsDef2,
            OneOfTransportGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "transportGateway"})


@dataclass
class OmpPayload:
    """
    OMP profile parcel schema for PUT request
    """

    data: SdwanSystemOmpData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanSystemOmpPayload:
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
    # OMP profile parcel schema for PUT request
    payload: Optional[OmpPayload] = _field(default=None)


@dataclass
class EditOmpProfileParcelForSystemPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemOmpOneOfOverlayAsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemOmpOneOfSendPathLimitOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemOmpOneOfEcmpLimitOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemOmpOneOfOmpAdminDistanceIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemOmpOneOfOmpAdminDistanceIpv4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[int] = _field(default=251)


@dataclass
class SystemOmpOneOfOmpAdminDistanceIpv6OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemOmpOneOfOmpAdminDistanceIpv6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[int] = _field(default=251)


@dataclass
class SystemOmpOneOfAdvertisementIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemOmpOneOfGracefulRestartTimerOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemOmpOneOfEorTimerOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemOmpOneOfHoldtimeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanSystemOmpOneOfAdvertiseConnectedOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # use enum for backward compatibility, use default for UI to display default value
    value: Optional[bool] = _field(default=True)


@dataclass
class SdwanSystemOmpOneOfAdvertiseStaticOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # use enum for backward compatibility, use default for UI to display default value
    value: Optional[bool] = _field(default=True)


@dataclass
class SystemOmpAdvertiseIpv4:
    bgp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    connected: Union[
        OneOfAdvertiseConnectedOptionsDef1,
        OneOfAdvertiseConnectedOptionsDef2,
        SdwanSystemOmpOneOfAdvertiseConnectedOptionsDef3,
    ]
    eigrp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    isis: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    lisp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    ospf: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    ospfv3: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    static: Union[
        OneOfAdvertiseStaticOptionsDef1,
        OneOfAdvertiseStaticOptionsDef2,
        SdwanSystemOmpOneOfAdvertiseStaticOptionsDef3,
    ]


@dataclass
class FeatureProfileSdwanSystemOmpOneOfAdvertiseConnectedOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # use enum for backward compatibility, use default for UI to display default value
    value: Optional[bool] = _field(default=True)


@dataclass
class FeatureProfileSdwanSystemOmpOneOfAdvertiseStaticOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # use enum for backward compatibility, use default for UI to display default value
    value: Optional[bool] = _field(default=True)


@dataclass
class SystemOmpAdvertiseIpv6:
    bgp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    connected: Union[
        OneOfAdvertiseConnectedOptionsDef1,
        OneOfAdvertiseConnectedOptionsDef2,
        FeatureProfileSdwanSystemOmpOneOfAdvertiseConnectedOptionsDef3,
    ]
    eigrp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    isis: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    lisp: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    ospf: Union[
        OneOfAdvertiseProtocolOptionsDef1,
        OneOfAdvertiseProtocolOptionsDef2,
        OneOfAdvertiseProtocolOptionsDef3,
    ]
    static: Union[
        OneOfAdvertiseStaticOptionsDef1,
        OneOfAdvertiseStaticOptionsDef2,
        FeatureProfileSdwanSystemOmpOneOfAdvertiseStaticOptionsDef3,
    ]


@dataclass
class SystemOmpOneOfTransportGatewayOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemOmpTransportGatewayEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanSystemOmpOneOfSiteTypesOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[SdwanSystemOmpSiteTypeListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdwanSystemOmpOneOfSiteTypesOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[
        FeatureProfileSdwanSystemOmpSiteTypeListDef
    ]  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdwanSystemOmpData:
    advertise_ipv4: SystemOmpAdvertiseIpv4 = _field(metadata={"alias": "advertiseIpv4"})
    advertise_ipv6: SystemOmpAdvertiseIpv6 = _field(metadata={"alias": "advertiseIpv6"})
    advertisement_interval: Union[
        OneOfAdvertisementIntervalOptionsDef1,
        SystemOmpOneOfAdvertisementIntervalOptionsDef2,
        OneOfAdvertisementIntervalOptionsDef3,
    ] = _field(metadata={"alias": "advertisementInterval"})
    ecmp_limit: Union[
        OneOfEcmpLimitOptionsDef1, SystemOmpOneOfEcmpLimitOptionsDef2, OneOfEcmpLimitOptionsDef3
    ] = _field(metadata={"alias": "ecmpLimit"})
    eor_timer: Union[
        OneOfEorTimerOptionsDef1, SystemOmpOneOfEorTimerOptionsDef2, OneOfEorTimerOptionsDef3
    ] = _field(metadata={"alias": "eorTimer"})
    graceful_restart: Union[
        OneOfGracefulRestartOptionsDef1,
        OneOfGracefulRestartOptionsDef2,
        OneOfGracefulRestartOptionsDef3,
    ] = _field(metadata={"alias": "gracefulRestart"})
    graceful_restart_timer: Union[
        OneOfGracefulRestartTimerOptionsDef1,
        SystemOmpOneOfGracefulRestartTimerOptionsDef2,
        OneOfGracefulRestartTimerOptionsDef3,
    ] = _field(metadata={"alias": "gracefulRestartTimer"})
    holdtime: Union[
        OneOfHoldtimeOptionsDef1, SystemOmpOneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3
    ]
    omp_admin_distance_ipv4: Union[
        OneOfOmpAdminDistanceIpv4OptionsDef1,
        SystemOmpOneOfOmpAdminDistanceIpv4OptionsDef2,
        SystemOmpOneOfOmpAdminDistanceIpv4OptionsDef3,
    ] = _field(metadata={"alias": "ompAdminDistanceIpv4"})
    omp_admin_distance_ipv6: Union[
        OneOfOmpAdminDistanceIpv6OptionsDef1,
        SystemOmpOneOfOmpAdminDistanceIpv6OptionsDef2,
        SystemOmpOneOfOmpAdminDistanceIpv6OptionsDef3,
    ] = _field(metadata={"alias": "ompAdminDistanceIpv6"})
    overlay_as: Union[
        OneOfOverlayAsOptionsDef1, SystemOmpOneOfOverlayAsOptionsDef2, OneOfOverlayAsOptionsDef3
    ] = _field(metadata={"alias": "overlayAs"})
    send_path_limit: Union[
        OneOfSendPathLimitOptionsDef1,
        SystemOmpOneOfSendPathLimitOptionsDef2,
        OneOfSendPathLimitOptionsDef3,
    ] = _field(metadata={"alias": "sendPathLimit"})
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    aspath_auto_translation: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "aspathAutoTranslation"})
    ignore_region_path_length: Optional[
        Union[
            OneOfIgnoreRegionPathLengthOptionsDef1,
            OneOfIgnoreRegionPathLengthOptionsDef2,
            OneOfIgnoreRegionPathLengthOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ignoreRegionPathLength"})
    site_types: Optional[
        Union[
            OneOfSiteTypesOptionsDef1,
            FeatureProfileSdwanSystemOmpOneOfSiteTypesOptionsDef2,
            OneOfSiteTypesOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "siteTypes"})
    site_types_for_transport_gateway: Optional[
        Union[
            OneOfSiteTypesOptionsDef1,
            SdwanSystemOmpOneOfSiteTypesOptionsDef2,
            OneOfSiteTypesOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "siteTypesForTransportGateway"})
    transport_gateway: Optional[
        Union[
            OneOfTransportGatewayOptionsDef1,
            SystemOmpOneOfTransportGatewayOptionsDef2,
            OneOfTransportGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "transportGateway"})


@dataclass
class EditOmpProfileParcelForSystemPutRequest:
    """
    OMP profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanSystemOmpData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
