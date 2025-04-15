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
class SsidConfig:
    qos_settings: Optional[str] = _field(default=None, metadata={"alias": "qosSettings"})
    security_auth_type: Optional[str] = _field(default=None, metadata={"alias": "securityAuthType"})
    ssid: Optional[str] = _field(default=None)
    visibility: Optional[bool] = _field(default=None)
    wpa_psk_key: Optional[str] = _field(default=None, metadata={"alias": "wpaPskKey"})


@dataclass
class GuestWifi:
    security_auth_type: Optional[str] = _field(default=None, metadata={"alias": "securityAuthType"})
    ssid: Optional[str] = _field(default=None)
    visibility: Optional[bool] = _field(default=None)
    wpa_psk_key: Optional[str] = _field(default=None, metadata={"alias": "wpaPskKey"})


@dataclass
class AaaServerInfo:
    aaa_servers_parcel_id: str = _field(metadata={"alias": "aaaServersParcelId"})
    radius_server_name: str = _field(metadata={"alias": "radiusServerName"})


@dataclass
class RadiusServer:
    host: str
    port: int
    secret: str


@dataclass
class CorporateWifi:
    security_auth_type: str = _field(metadata={"alias": "securityAuthType"})
    aaa_server_info: Optional[AaaServerInfo] = _field(
        default=None, metadata={"alias": "aaaServerInfo"}
    )
    corporate_wlan: Optional[bool] = _field(default=None, metadata={"alias": "corporateWlan"})
    radius_server: Optional[RadiusServer] = _field(default=None, metadata={"alias": "radiusServer"})
    ssid: Optional[str] = _field(default=None)
    visibility: Optional[bool] = _field(default=None)
    wpa_psk_key: Optional[str] = _field(default=None, metadata={"alias": "wpaPskKey"})


@dataclass
class RadioBandSetting24G:
    band: Optional[str] = _field(default=None)
    channel: Optional[str] = _field(default=None)
    channel_width: Optional[str] = _field(default=None, metadata={"alias": "channelWidth"})
    transmit_power: Optional[str] = _field(default=None, metadata={"alias": "transmitPower"})


@dataclass
class RadioBandSetting5G:
    band: Optional[str] = _field(default=None)
    channel: Optional[str] = _field(default=None)
    channel_width: Optional[str] = _field(default=None, metadata={"alias": "channelWidth"})
    transmit_power: Optional[str] = _field(default=None, metadata={"alias": "transmitPower"})


@dataclass
class ChannelPowerSettings:
    radio_band2_dot4_ghz: Optional[RadioBandSetting24G] = _field(
        default=None, metadata={"alias": "radioBand2Dot4Ghz"}
    )
    radio_band5_ghz: Optional[RadioBandSetting5G] = _field(
        default=None, metadata={"alias": "radioBand5Ghz"}
    )


@dataclass
class CountryRegionSettings:
    country_region: Optional[str] = _field(default=None, metadata={"alias": "countryRegion"})
    regulatory_domain: Optional[str] = _field(default=None, metadata={"alias": "regulatoryDomain"})


@dataclass
class AdvancedRadioSetting:
    channel_power_settings: Optional[ChannelPowerSettings] = _field(
        default=None, metadata={"alias": "channelPowerSettings"}
    )
    country_region_settings: Optional[CountryRegionSettings] = _field(
        default=None, metadata={"alias": "countryRegionSettings"}
    )


@dataclass
class Wifi:
    # Name of the Profile Parcel. Must be unique.
    name: str
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    advanced_radio_setting: Optional[AdvancedRadioSetting] = _field(
        default=None, metadata={"alias": "advancedRadioSetting"}
    )
    corporate_wifi: Optional[CorporateWifi] = _field(
        default=None, metadata={"alias": "corporateWifi"}
    )
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    guest_wifi: Optional[GuestWifi] = _field(default=None, metadata={"alias": "guestWifi"})
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    ssid_config_list: Optional[List[SsidConfig]] = _field(
        default=None, metadata={"alias": "ssidConfigList"}
    )
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
    payload: Optional[Wifi] = _field(default=None)


@dataclass
class GetListMobilityGlobalWifiPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateWifiProfileParcelForMobilityPostRequest:
    # Name of the Profile Parcel. Must be unique.
    name: str
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    advanced_radio_setting: Optional[AdvancedRadioSetting] = _field(
        default=None, metadata={"alias": "advancedRadioSetting"}
    )
    corporate_wifi: Optional[CorporateWifi] = _field(
        default=None, metadata={"alias": "corporateWifi"}
    )
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    guest_wifi: Optional[GuestWifi] = _field(default=None, metadata={"alias": "guestWifi"})
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    ssid_config_list: Optional[List[SsidConfig]] = _field(
        default=None, metadata={"alias": "ssidConfigList"}
    )
    variables: Optional[List[Variable]] = _field(default=None)


@dataclass
class GetSingleMobilityGlobalWifiPayload:
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
    payload: Optional[Wifi] = _field(default=None)


@dataclass
class EditWifiProfileParcelForMobilityPutRequest:
    # Name of the Profile Parcel. Must be unique.
    name: str
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    advanced_radio_setting: Optional[AdvancedRadioSetting] = _field(
        default=None, metadata={"alias": "advancedRadioSetting"}
    )
    corporate_wifi: Optional[CorporateWifi] = _field(
        default=None, metadata={"alias": "corporateWifi"}
    )
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    guest_wifi: Optional[GuestWifi] = _field(default=None, metadata={"alias": "guestWifi"})
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    ssid_config_list: Optional[List[SsidConfig]] = _field(
        default=None, metadata={"alias": "ssidConfigList"}
    )
    variables: Optional[List[Variable]] = _field(default=None)
