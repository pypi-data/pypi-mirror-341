# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

SsidRadioTypeDef = Literal["24ghz", "5ghz", "all"]

DefaultSsidRadioTypeDef = Literal["all"]

SsidQosProfileDef = Literal["bronze", "gold", "platinum", "silver"]

DefaultSsidQosProfileDef = Literal["silver"]

CountryDef = Literal[
    "AE",
    "AR",
    "AT",
    "AU",
    "BA",
    "BB",
    "BE",
    "BG",
    "BH",
    "BN",
    "BO",
    "BR",
    "BY",
    "CA",
    "CA2",
    "CH",
    "CL",
    "CM",
    "CN",
    "CO",
    "CR",
    "CY",
    "CZ",
    "DE",
    "DK",
    "DO",
    "DZ",
    "EC",
    "EE",
    "EG",
    "ES",
    "FI",
    "FJ",
    "FR",
    "GB",
    "GH",
    "GI",
    "GR",
    "HK",
    "HR",
    "HU",
    "ID",
    "IE",
    "IL",
    "IN",
    "IO",
    "IQ",
    "IS",
    "IT",
    "J2",
    "J4",
    "JM",
    "JO",
    "KE",
    "KN",
    "KW",
    "KZ",
    "LB",
    "LI",
    "LK",
    "LT",
    "LU",
    "LV",
    "LY",
    "MA",
    "MC",
    "ME",
    "MK",
    "MN",
    "MO",
    "MT",
    "MX",
    "MY",
    "NL",
    "NO",
    "NZ",
    "OM",
    "PA",
    "PE",
    "PH",
    "PH2",
    "PK",
    "PL",
    "PR",
    "PT",
    "PY",
    "QA",
    "RO",
    "RS",
    "RU",
    "SA",
    "SE",
    "SG",
    "SI",
    "SK",
    "TH",
    "TN",
    "TR",
    "TW",
    "UA",
    "US",
    "UY",
    "VE",
    "VN",
    "ZA",
]

OptionType = Literal["default", "global"]

Ipv4SubnetMaskDef = Literal[
    "0.0.0.0",
    "128.0.0.0",
    "192.0.0.0",
    "224.0.0.0",
    "240.0.0.0",
    "248.0.0.0",
    "252.0.0.0",
    "254.0.0.0",
    "255.0.0.0",
    "255.128.0.0",
    "255.192.0.0",
    "255.224.0.0",
    "255.240.0.0",
    "255.252.0.0",
    "255.254.0.0",
    "255.255.0.0",
    "255.255.128.0",
    "255.255.192.0",
    "255.255.224.0",
    "255.255.240.0",
    "255.255.248.0",
    "255.255.252.0",
    "255.255.254.0",
    "255.255.255.0",
    "255.255.255.128",
    "255.255.255.192",
    "255.255.255.224",
    "255.255.255.240",
    "255.255.255.248",
    "255.255.255.252",
    "255.255.255.254",
    "255.255.255.255",
]

WirelesslanSsidRadioTypeDef = Literal["24ghz", "5ghz", "all"]

WirelesslanDefaultSsidRadioTypeDef = Literal["all"]

WirelesslanSsidQosProfileDef = Literal["bronze", "gold", "platinum", "silver"]

WirelesslanDefaultSsidQosProfileDef = Literal["silver"]

WirelesslanCountryDef = Literal[
    "AE",
    "AR",
    "AT",
    "AU",
    "BA",
    "BB",
    "BE",
    "BG",
    "BH",
    "BN",
    "BO",
    "BR",
    "BY",
    "CA",
    "CA2",
    "CH",
    "CL",
    "CM",
    "CN",
    "CO",
    "CR",
    "CY",
    "CZ",
    "DE",
    "DK",
    "DO",
    "DZ",
    "EC",
    "EE",
    "EG",
    "ES",
    "FI",
    "FJ",
    "FR",
    "GB",
    "GH",
    "GI",
    "GR",
    "HK",
    "HR",
    "HU",
    "ID",
    "IE",
    "IL",
    "IN",
    "IO",
    "IQ",
    "IS",
    "IT",
    "J2",
    "J4",
    "JM",
    "JO",
    "KE",
    "KN",
    "KW",
    "KZ",
    "LB",
    "LI",
    "LK",
    "LT",
    "LU",
    "LV",
    "LY",
    "MA",
    "MC",
    "ME",
    "MK",
    "MN",
    "MO",
    "MT",
    "MX",
    "MY",
    "NL",
    "NO",
    "NZ",
    "OM",
    "PA",
    "PE",
    "PH",
    "PH2",
    "PK",
    "PL",
    "PR",
    "PT",
    "PY",
    "QA",
    "RO",
    "RS",
    "RU",
    "SA",
    "SE",
    "SG",
    "SI",
    "SK",
    "TH",
    "TN",
    "TR",
    "TW",
    "UA",
    "US",
    "UY",
    "VE",
    "VN",
    "ZA",
]

ServiceWirelesslanSsidRadioTypeDef = Literal["24ghz", "5ghz", "all"]

ServiceWirelesslanDefaultSsidRadioTypeDef = Literal["all"]

ServiceWirelesslanSsidQosProfileDef = Literal["bronze", "gold", "platinum", "silver"]

ServiceWirelesslanDefaultSsidQosProfileDef = Literal["silver"]

ServiceWirelesslanCountryDef = Literal[
    "AE",
    "AR",
    "AT",
    "AU",
    "BA",
    "BB",
    "BE",
    "BG",
    "BH",
    "BN",
    "BO",
    "BR",
    "BY",
    "CA",
    "CA2",
    "CH",
    "CL",
    "CM",
    "CN",
    "CO",
    "CR",
    "CY",
    "CZ",
    "DE",
    "DK",
    "DO",
    "DZ",
    "EC",
    "EE",
    "EG",
    "ES",
    "FI",
    "FJ",
    "FR",
    "GB",
    "GH",
    "GI",
    "GR",
    "HK",
    "HR",
    "HU",
    "ID",
    "IE",
    "IL",
    "IN",
    "IO",
    "IQ",
    "IS",
    "IT",
    "J2",
    "J4",
    "JM",
    "JO",
    "KE",
    "KN",
    "KW",
    "KZ",
    "LB",
    "LI",
    "LK",
    "LT",
    "LU",
    "LV",
    "LY",
    "MA",
    "MC",
    "ME",
    "MK",
    "MN",
    "MO",
    "MT",
    "MX",
    "MY",
    "NL",
    "NO",
    "NZ",
    "OM",
    "PA",
    "PE",
    "PH",
    "PH2",
    "PK",
    "PL",
    "PR",
    "PT",
    "PY",
    "QA",
    "RO",
    "RS",
    "RU",
    "SA",
    "SE",
    "SG",
    "SI",
    "SK",
    "TH",
    "TN",
    "TR",
    "TW",
    "UA",
    "US",
    "UY",
    "VE",
    "VN",
    "ZA",
]


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSsidNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSsidVlanIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSsidVlanIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSsidRadioTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SsidRadioTypeDef


@dataclass
class OneOfSsidRadioTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSsidRadioTypeOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[DefaultSsidRadioTypeDef] = _field(default=None)


@dataclass
class SecurityType:
    """
    Select security type
    """

    option_type: Any = _field(metadata={"alias": "optionType"})
    value: Any


@dataclass
class OneOfIpV4AddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfSsidRadiusServerPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSsidRadiusServerPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSsidRadiusServerPortOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfSsidRadiusServerSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSsidRadiusServerSecretOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSsidPassphraseOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSsidPassphraseOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SecurityConfig1:
    # Select security type
    security_type: SecurityType = _field(metadata={"alias": "securityType"})
    passphrase: Optional[Union[OneOfSsidPassphraseOptionsDef1, OneOfSsidPassphraseOptionsDef2]] = (
        _field(default=None)
    )
    radius_server_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "radiusServerIp"})
    )
    radius_server_port: Optional[
        Union[
            OneOfSsidRadiusServerPortOptionsDef1,
            OneOfSsidRadiusServerPortOptionsDef2,
            OneOfSsidRadiusServerPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "radiusServerPort"})
    radius_server_secret: Optional[
        Union[OneOfSsidRadiusServerSecretOptionsDef1, OneOfSsidRadiusServerSecretOptionsDef2]
    ] = _field(default=None, metadata={"alias": "radiusServerSecret"})


@dataclass
class WirelesslanSecurityType:
    """
    Select security type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SecurityConfig2:
    # Select security type
    security_type: WirelesslanSecurityType = _field(metadata={"alias": "securityType"})
    passphrase: Optional[Union[OneOfSsidPassphraseOptionsDef1, OneOfSsidPassphraseOptionsDef2]] = (
        _field(default=None)
    )
    radius_server_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "radiusServerIp"})
    )
    radius_server_port: Optional[
        Union[
            OneOfSsidRadiusServerPortOptionsDef1,
            OneOfSsidRadiusServerPortOptionsDef2,
            OneOfSsidRadiusServerPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "radiusServerPort"})
    radius_server_secret: Optional[
        Union[OneOfSsidRadiusServerSecretOptionsDef1, OneOfSsidRadiusServerSecretOptionsDef2]
    ] = _field(default=None, metadata={"alias": "radiusServerSecret"})


@dataclass
class OneOfSsidQosProfileOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SsidQosProfileDef


@dataclass
class OneOfSsidQosProfileOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSsidQosProfileOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[DefaultSsidQosProfileDef] = _field(default=None)


@dataclass
class Ssid:
    admin_state: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "adminState"})
    broadcast_ssid: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "broadcastSsid"})
    name: OneOfSsidNameOptionsDef
    qos_profile: Union[
        OneOfSsidQosProfileOptionsDef1,
        OneOfSsidQosProfileOptionsDef2,
        OneOfSsidQosProfileOptionsDef3,
    ] = _field(metadata={"alias": "qosProfile"})
    radio_type: Union[
        OneOfSsidRadioTypeOptionsDef1, OneOfSsidRadioTypeOptionsDef2, OneOfSsidRadioTypeOptionsDef3
    ] = _field(metadata={"alias": "radioType"})
    # Select security type
    security_config: Union[SecurityConfig1, SecurityConfig2] = _field(
        metadata={"alias": "securityConfig"}
    )
    vlan_id: Union[OneOfSsidVlanIdOptionsDef1, OneOfSsidVlanIdOptionsDef2] = _field(
        metadata={"alias": "vlanId"}
    )


@dataclass
class OneOfCountryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CountryDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCountryOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUsernameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfPasswordOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class MeDynamicIpEnabled:
    """
    ME management IP dynamic allocated by DHCP
    """

    option_type: OptionType = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class MeIpConfig1:
    # ME management IP dynamic allocated by DHCP
    me_dynamic_ip_enabled: MeDynamicIpEnabled = _field(metadata={"alias": "meDynamicIpEnabled"})


@dataclass
class BooleanGlobalFalseOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpV4SubnetMaskOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4SubnetMaskOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class MeStaticIpCfg:
    """
    Mobility Express management IP static configuration
    """

    default_gateway: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "defaultGateway"}
    )
    me_ipv4_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "meIpv4Address"}
    )
    netmask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]


@dataclass
class MeIpConfig2:
    me_dynamic_ip_enabled: BooleanGlobalFalseOptionsDef = _field(
        metadata={"alias": "meDynamicIpEnabled"}
    )
    # Mobility Express management IP static configuration
    me_static_ip_cfg: MeStaticIpCfg = _field(metadata={"alias": "meStaticIpCfg"})


@dataclass
class WirelesslanData:
    country: Union[OneOfCountryOptionsDef1, OneOfCountryOptionsDef2]
    enable24_g: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "enable24G"})
    enable5_g: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "enable5G"})
    # ME management IP configuration, if ME IP address is assigned by DHCP, a DHCP server parcel, a Wlan-GigabitEthernet switchport parcel, and a management SVI interface parcel must be created and associate with configuration group.
    me_ip_config: Union[MeIpConfig1, MeIpConfig2] = _field(metadata={"alias": "meIpConfig"})
    password: Union[OneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    # Configure Wi-Fi SSID profile
    ssid: List[Ssid]
    username: Union[OneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class Payload:
    """
    wirelesslan profile parcel schema for POST request
    """

    data: WirelesslanData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


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
    # wirelesslan profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanServiceWirelesslanPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateWirelesslanProfileParcelForServicePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceWirelesslanData:
    country: Union[OneOfCountryOptionsDef1, OneOfCountryOptionsDef2]
    enable24_g: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "enable24G"})
    enable5_g: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "enable5G"})
    # ME management IP configuration, if ME IP address is assigned by DHCP, a DHCP server parcel, a Wlan-GigabitEthernet switchport parcel, and a management SVI interface parcel must be created and associate with configuration group.
    me_ip_config: Union[MeIpConfig1, MeIpConfig2] = _field(metadata={"alias": "meIpConfig"})
    password: Union[OneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    # Configure Wi-Fi SSID profile
    ssid: List[Ssid]
    username: Union[OneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class CreateWirelesslanProfileParcelForServicePostRequest:
    """
    wirelesslan profile parcel schema for POST request
    """

    data: ServiceWirelesslanData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class WirelesslanOneOfSsidNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WirelesslanOneOfSsidVlanIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WirelesslanOneOfSsidRadioTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WirelesslanSsidRadioTypeDef


@dataclass
class WirelesslanOneOfSsidRadioTypeOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[WirelesslanDefaultSsidRadioTypeDef] = _field(default=None)


@dataclass
class WirelesslanOneOfSsidRadiusServerPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WirelesslanOneOfSsidRadiusServerPortOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class WirelesslanOneOfSsidRadiusServerSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WirelesslanOneOfSsidPassphraseOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WirelesslanSecurityConfig1:
    # Select security type
    security_type: SecurityType = _field(metadata={"alias": "securityType"})
    passphrase: Optional[
        Union[WirelesslanOneOfSsidPassphraseOptionsDef1, OneOfSsidPassphraseOptionsDef2]
    ] = _field(default=None)
    radius_server_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "radiusServerIp"})
    )
    radius_server_port: Optional[
        Union[
            WirelesslanOneOfSsidRadiusServerPortOptionsDef1,
            OneOfSsidRadiusServerPortOptionsDef2,
            WirelesslanOneOfSsidRadiusServerPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "radiusServerPort"})
    radius_server_secret: Optional[
        Union[
            WirelesslanOneOfSsidRadiusServerSecretOptionsDef1,
            OneOfSsidRadiusServerSecretOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "radiusServerSecret"})


@dataclass
class ServiceWirelesslanSecurityType:
    """
    Select security type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class ServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class ServiceWirelesslanOneOfSsidRadiusServerSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceWirelesslanOneOfSsidPassphraseOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WirelesslanSecurityConfig2:
    # Select security type
    security_type: ServiceWirelesslanSecurityType = _field(metadata={"alias": "securityType"})
    passphrase: Optional[
        Union[ServiceWirelesslanOneOfSsidPassphraseOptionsDef1, OneOfSsidPassphraseOptionsDef2]
    ] = _field(default=None)
    radius_server_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "radiusServerIp"})
    )
    radius_server_port: Optional[
        Union[
            ServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef1,
            OneOfSsidRadiusServerPortOptionsDef2,
            ServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "radiusServerPort"})
    radius_server_secret: Optional[
        Union[
            ServiceWirelesslanOneOfSsidRadiusServerSecretOptionsDef1,
            OneOfSsidRadiusServerSecretOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "radiusServerSecret"})


@dataclass
class WirelesslanOneOfSsidQosProfileOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WirelesslanSsidQosProfileDef


@dataclass
class WirelesslanOneOfSsidQosProfileOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[WirelesslanDefaultSsidQosProfileDef] = _field(default=None)


@dataclass
class WirelesslanSsid:
    admin_state: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "adminState"})
    broadcast_ssid: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "broadcastSsid"})
    name: WirelesslanOneOfSsidNameOptionsDef
    qos_profile: Union[
        WirelesslanOneOfSsidQosProfileOptionsDef1,
        OneOfSsidQosProfileOptionsDef2,
        WirelesslanOneOfSsidQosProfileOptionsDef3,
    ] = _field(metadata={"alias": "qosProfile"})
    radio_type: Union[
        WirelesslanOneOfSsidRadioTypeOptionsDef1,
        OneOfSsidRadioTypeOptionsDef2,
        WirelesslanOneOfSsidRadioTypeOptionsDef3,
    ] = _field(metadata={"alias": "radioType"})
    # Select security type
    security_config: Union[WirelesslanSecurityConfig1, WirelesslanSecurityConfig2] = _field(
        metadata={"alias": "securityConfig"}
    )
    vlan_id: Union[WirelesslanOneOfSsidVlanIdOptionsDef1, OneOfSsidVlanIdOptionsDef2] = _field(
        metadata={"alias": "vlanId"}
    )


@dataclass
class WirelesslanOneOfCountryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WirelesslanCountryDef  # pytype: disable=annotation-type-mismatch


@dataclass
class WirelesslanOneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WirelesslanOneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SdwanServiceWirelesslanData:
    country: Union[WirelesslanOneOfCountryOptionsDef1, OneOfCountryOptionsDef2]
    enable24_g: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "enable24G"})
    enable5_g: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "enable5G"})
    # ME management IP configuration, if ME IP address is assigned by DHCP, a DHCP server parcel, a Wlan-GigabitEthernet switchport parcel, and a management SVI interface parcel must be created and associate with configuration group.
    me_ip_config: Union[MeIpConfig1, MeIpConfig2] = _field(metadata={"alias": "meIpConfig"})
    password: Union[WirelesslanOneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    # Configure Wi-Fi SSID profile
    ssid: List[WirelesslanSsid]
    username: Union[WirelesslanOneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class WirelesslanPayload:
    """
    wirelesslan profile parcel schema for PUT request
    """

    data: SdwanServiceWirelesslanData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanServiceWirelesslanPayload:
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
    # wirelesslan profile parcel schema for PUT request
    payload: Optional[WirelesslanPayload] = _field(default=None)


@dataclass
class EditWirelesslanProfileParcelForServicePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceWirelesslanOneOfSsidNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceWirelesslanOneOfSsidVlanIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceWirelesslanOneOfSsidRadioTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceWirelesslanSsidRadioTypeDef


@dataclass
class ServiceWirelesslanOneOfSsidRadioTypeOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[ServiceWirelesslanDefaultSsidRadioTypeDef] = _field(default=None)


@dataclass
class SdwanServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SdwanServiceWirelesslanOneOfSsidRadiusServerSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanServiceWirelesslanOneOfSsidPassphraseOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceWirelesslanSecurityConfig1:
    # Select security type
    security_type: SecurityType = _field(metadata={"alias": "securityType"})
    passphrase: Optional[
        Union[SdwanServiceWirelesslanOneOfSsidPassphraseOptionsDef1, OneOfSsidPassphraseOptionsDef2]
    ] = _field(default=None)
    radius_server_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "radiusServerIp"})
    )
    radius_server_port: Optional[
        Union[
            SdwanServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef1,
            OneOfSsidRadiusServerPortOptionsDef2,
            SdwanServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "radiusServerPort"})
    radius_server_secret: Optional[
        Union[
            SdwanServiceWirelesslanOneOfSsidRadiusServerSecretOptionsDef1,
            OneOfSsidRadiusServerSecretOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "radiusServerSecret"})


@dataclass
class SdwanServiceWirelesslanSecurityType:
    """
    Select security type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class FeatureProfileSdwanServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class FeatureProfileSdwanServiceWirelesslanOneOfSsidRadiusServerSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanServiceWirelesslanOneOfSsidPassphraseOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceWirelesslanSecurityConfig2:
    # Select security type
    security_type: SdwanServiceWirelesslanSecurityType = _field(metadata={"alias": "securityType"})
    passphrase: Optional[
        Union[
            FeatureProfileSdwanServiceWirelesslanOneOfSsidPassphraseOptionsDef1,
            OneOfSsidPassphraseOptionsDef2,
        ]
    ] = _field(default=None)
    radius_server_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "radiusServerIp"})
    )
    radius_server_port: Optional[
        Union[
            FeatureProfileSdwanServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef1,
            OneOfSsidRadiusServerPortOptionsDef2,
            FeatureProfileSdwanServiceWirelesslanOneOfSsidRadiusServerPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "radiusServerPort"})
    radius_server_secret: Optional[
        Union[
            FeatureProfileSdwanServiceWirelesslanOneOfSsidRadiusServerSecretOptionsDef1,
            OneOfSsidRadiusServerSecretOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "radiusServerSecret"})


@dataclass
class ServiceWirelesslanOneOfSsidQosProfileOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceWirelesslanSsidQosProfileDef


@dataclass
class ServiceWirelesslanOneOfSsidQosProfileOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[ServiceWirelesslanDefaultSsidQosProfileDef] = _field(default=None)


@dataclass
class ServiceWirelesslanSsid:
    admin_state: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "adminState"})
    broadcast_ssid: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "broadcastSsid"})
    name: ServiceWirelesslanOneOfSsidNameOptionsDef
    qos_profile: Union[
        ServiceWirelesslanOneOfSsidQosProfileOptionsDef1,
        OneOfSsidQosProfileOptionsDef2,
        ServiceWirelesslanOneOfSsidQosProfileOptionsDef3,
    ] = _field(metadata={"alias": "qosProfile"})
    radio_type: Union[
        ServiceWirelesslanOneOfSsidRadioTypeOptionsDef1,
        OneOfSsidRadioTypeOptionsDef2,
        ServiceWirelesslanOneOfSsidRadioTypeOptionsDef3,
    ] = _field(metadata={"alias": "radioType"})
    # Select security type
    security_config: Union[ServiceWirelesslanSecurityConfig1, ServiceWirelesslanSecurityConfig2] = (
        _field(metadata={"alias": "securityConfig"})
    )
    vlan_id: Union[ServiceWirelesslanOneOfSsidVlanIdOptionsDef1, OneOfSsidVlanIdOptionsDef2] = (
        _field(metadata={"alias": "vlanId"})
    )


@dataclass
class ServiceWirelesslanOneOfCountryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceWirelesslanCountryDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceWirelesslanOneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceWirelesslanOneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class FeatureProfileSdwanServiceWirelesslanData:
    country: Union[ServiceWirelesslanOneOfCountryOptionsDef1, OneOfCountryOptionsDef2]
    enable24_g: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "enable24G"})
    enable5_g: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "enable5G"})
    # ME management IP configuration, if ME IP address is assigned by DHCP, a DHCP server parcel, a Wlan-GigabitEthernet switchport parcel, and a management SVI interface parcel must be created and associate with configuration group.
    me_ip_config: Union[MeIpConfig1, MeIpConfig2] = _field(metadata={"alias": "meIpConfig"})
    password: Union[ServiceWirelesslanOneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    # Configure Wi-Fi SSID profile
    ssid: List[ServiceWirelesslanSsid]
    username: Union[ServiceWirelesslanOneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class EditWirelesslanProfileParcelForServicePutRequest:
    """
    wirelesslan profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanServiceWirelesslanData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
