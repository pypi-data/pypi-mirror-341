# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

OptionType = Literal["variable"]


@dataclass
class OneOfVirtualApplicationTokenOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVirtualApplicationTokenOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVirtualApplicationVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVirtualApplicationVpnOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVirtualApplicationVpnOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class TeMgmtIp:
    option_type: Optional[OptionType] = _field(default=None, metadata={"alias": "optionType"})


@dataclass
class TeMgmtSubnetMask:
    option_type: Optional[OptionType] = _field(default=None, metadata={"alias": "optionType"})


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
    value: Union[Any, str]


@dataclass
class OneOfVirtualApplicationNameServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[Any, str]


@dataclass
class OneOfVirtualApplicationNameServerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVirtualApplicationNameServerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVirtualApplicationHostnameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVirtualApplicationHostnameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVirtualApplicationHostnameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class ProxyType:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfVirtualApplicationProxyHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVirtualApplicationProxyHostOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class ProxyConfig1:
    # Select Web Proxy Type
    proxy_type: ProxyType = _field(metadata={"alias": "proxyType"})
    proxy_host: Optional[
        Union[
            OneOfVirtualApplicationProxyHostOptionsDef1, OneOfVirtualApplicationProxyHostOptionsDef2
        ]
    ] = _field(default=None, metadata={"alias": "proxyHost"})
    proxy_port: Optional[Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2]] = _field(
        default=None, metadata={"alias": "proxyPort"}
    )


@dataclass
class ThousandeyesProxyType:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfVirtualApplicationPacUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVirtualApplicationPacUrlOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class ProxyConfig2:
    # Select Web Proxy Type
    proxy_type: ThousandeyesProxyType = _field(metadata={"alias": "proxyType"})
    pac_url: Optional[
        Union[OneOfVirtualApplicationPacUrlOptionsDef1, OneOfVirtualApplicationPacUrlOptionsDef2]
    ] = _field(default=None, metadata={"alias": "pacUrl"})


@dataclass
class OtherThousandeyesProxyType:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class ProxyConfig3:
    # Select Web Proxy Type
    proxy_type: OtherThousandeyesProxyType = _field(metadata={"alias": "proxyType"})


@dataclass
class SdwanOtherThousandeyesProxyType:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class VariableOptionTypeObjectDef:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class ProxyConfig4:
    # Select Web Proxy Type
    proxy_type: SdwanOtherThousandeyesProxyType = _field(metadata={"alias": "proxyType"})
    pac_url: Optional[VariableOptionTypeObjectDef] = _field(
        default=None, metadata={"alias": "pacUrl"}
    )
    proxy_host: Optional[VariableOptionTypeObjectDef] = _field(
        default=None, metadata={"alias": "proxyHost"}
    )
    proxy_port: Optional[VariableOptionTypeObjectDef] = _field(
        default=None, metadata={"alias": "proxyPort"}
    )


@dataclass
class VirtualApplication1:
    # Web Proxy Type Config
    proxy_config: Union[ProxyConfig1, ProxyConfig2, ProxyConfig3, ProxyConfig4] = _field(
        metadata={"alias": "proxyConfig"}
    )
    token: Union[OneOfVirtualApplicationTokenOptionsDef1, OneOfVirtualApplicationTokenOptionsDef2]
    hostname: Optional[
        Union[
            OneOfVirtualApplicationHostnameOptionsDef1,
            OneOfVirtualApplicationHostnameOptionsDef2,
            OneOfVirtualApplicationHostnameOptionsDef3,
        ]
    ] = _field(default=None)
    name_server: Optional[
        Union[
            OneOfVirtualApplicationNameServerOptionsDef1,
            OneOfVirtualApplicationNameServerOptionsDef2,
            OneOfVirtualApplicationNameServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nameServer"})
    name_server1: Optional[
        Union[
            OneOfVirtualApplicationNameServerOptionsDef1,
            OneOfVirtualApplicationNameServerOptionsDef2,
            OneOfVirtualApplicationNameServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nameServer1"})
    te_mgmt_ip: Optional[TeMgmtIp] = _field(default=None, metadata={"alias": "teMgmtIp"})
    te_mgmt_subnet_mask: Optional[TeMgmtSubnetMask] = _field(
        default=None, metadata={"alias": "teMgmtSubnetMask"}
    )
    te_vpg_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teVpgIp"}
    )
    vpn: Optional[
        Union[
            OneOfVirtualApplicationVpnOptionsDef1,
            OneOfVirtualApplicationVpnOptionsDef2,
            OneOfVirtualApplicationVpnOptionsDef3,
        ]
    ] = _field(default=None)


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
    value: str


@dataclass
class VirtualApplication2:
    # Web Proxy Type Config
    proxy_config: Union[ProxyConfig1, ProxyConfig2, ProxyConfig3, ProxyConfig4] = _field(
        metadata={"alias": "proxyConfig"}
    )
    token: Union[OneOfVirtualApplicationTokenOptionsDef1, OneOfVirtualApplicationTokenOptionsDef2]
    hostname: Optional[
        Union[
            OneOfVirtualApplicationHostnameOptionsDef1,
            OneOfVirtualApplicationHostnameOptionsDef2,
            OneOfVirtualApplicationHostnameOptionsDef3,
        ]
    ] = _field(default=None)
    name_server: Optional[
        Union[
            OneOfVirtualApplicationNameServerOptionsDef1,
            OneOfVirtualApplicationNameServerOptionsDef2,
            OneOfVirtualApplicationNameServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nameServer"})
    name_server1: Optional[
        Union[
            OneOfVirtualApplicationNameServerOptionsDef1,
            OneOfVirtualApplicationNameServerOptionsDef2,
            OneOfVirtualApplicationNameServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nameServer1"})
    te_mgmt_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teMgmtIp"}
    )
    te_mgmt_subnet_mask: Optional[
        Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]
    ] = _field(default=None, metadata={"alias": "teMgmtSubnetMask"})
    te_vpg_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teVpgIp"}
    )
    vpn: Optional[
        Union[
            OneOfVirtualApplicationVpnOptionsDef1,
            OneOfVirtualApplicationVpnOptionsDef2,
            OneOfVirtualApplicationVpnOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class ThousandeyesData:
    # Virtual application Instance
    virtual_application: Optional[List[Union[VirtualApplication1, VirtualApplication2]]] = _field(
        default=None, metadata={"alias": "virtualApplication"}
    )


@dataclass
class Payload:
    """
    thousandeyes profile parcel schema for POST/PUT request
    """

    data: ThousandeyesData
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
    # thousandeyes profile parcel schema for POST/PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanOtherThousandeyesPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateThousandeyesProfileParcelForOtherPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OtherThousandeyesData:
    # Virtual application Instance
    virtual_application: Optional[List[Union[VirtualApplication1, VirtualApplication2]]] = _field(
        default=None, metadata={"alias": "virtualApplication"}
    )


@dataclass
class CreateThousandeyesProfileParcelForOtherPostRequest:
    """
    thousandeyes profile parcel schema for POST/PUT request
    """

    data: OtherThousandeyesData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanOtherThousandeyesPayload:
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
    # thousandeyes profile parcel schema for POST/PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditThousandeyesProfileParcelForOtherPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanOtherThousandeyesData:
    # Virtual application Instance
    virtual_application: Optional[List[Union[VirtualApplication1, VirtualApplication2]]] = _field(
        default=None, metadata={"alias": "virtualApplication"}
    )


@dataclass
class EditThousandeyesProfileParcelForOtherPutRequest:
    """
    thousandeyes profile parcel schema for POST/PUT request
    """

    data: SdwanOtherThousandeyesData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
