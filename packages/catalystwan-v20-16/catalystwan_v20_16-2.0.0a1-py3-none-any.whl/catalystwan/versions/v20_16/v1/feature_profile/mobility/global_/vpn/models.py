# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

LocalInterfaceDef = Literal["Cellular1/0", "GigabitEthernet0/0"]

DefaultOptionTypeDef = Literal["default"]

IkePhase1CipherSuiteDefaultDef = Literal["aes128-cbc-sha1"]

IkePhase1CipherSuiteDef = Literal[
    "aes128-cbc-sha1",
    "aes128-cbc-sha256",
    "aes128-gcm",
    "aes256-cbc-sha1",
    "aes256-cbc-sha256",
    "aes256-gcm",
]

DiffeHellmanGroupDef = Literal["14", "15", "16", "19", "20", "21"]

DiffeHellmanGroupDefaultDef = Literal["14"]

IkePhase2CipherSuiteDefaultDef = Literal["aes128-sha1"]

IkePhase2CipherSuiteDef = Literal[
    "aes128-cbc-sha1",
    "aes128-cbc-sha256",
    "aes128-gcm",
    "aes128-sha1",
    "aes256-cbc-sha1",
    "aes256-cbc-sha256",
    "aes256-gcm",
]

VpnLocalInterfaceDef = Literal["Cellular1/0", "GigabitEthernet0/0"]

VpnIkePhase1CipherSuiteDefaultDef = Literal["aes128-cbc-sha1"]

VpnIkePhase1CipherSuiteDef = Literal[
    "aes128-cbc-sha1",
    "aes128-cbc-sha256",
    "aes128-gcm",
    "aes256-cbc-sha1",
    "aes256-cbc-sha256",
    "aes256-gcm",
]

VpnDiffeHellmanGroupDef = Literal["14", "15", "16", "19", "20", "21"]

VpnDiffeHellmanGroupDefaultDef = Literal["14"]

VpnIkePhase2CipherSuiteDefaultDef = Literal["aes128-sha1"]

VpnIkePhase2CipherSuiteDef = Literal[
    "aes128-cbc-sha1",
    "aes128-cbc-sha256",
    "aes128-gcm",
    "aes128-sha1",
    "aes256-cbc-sha1",
    "aes256-cbc-sha256",
    "aes256-gcm",
]

GlobalVpnLocalInterfaceDef = Literal["Cellular1/0", "GigabitEthernet0/0"]

GlobalVpnIkePhase1CipherSuiteDefaultDef = Literal["aes128-cbc-sha1"]

GlobalVpnIkePhase1CipherSuiteDef = Literal[
    "aes128-cbc-sha1",
    "aes128-cbc-sha256",
    "aes128-gcm",
    "aes256-cbc-sha1",
    "aes256-cbc-sha256",
    "aes256-gcm",
]

GlobalVpnDiffeHellmanGroupDef = Literal["14", "15", "16", "19", "20", "21"]

GlobalVpnDiffeHellmanGroupDefaultDef = Literal["14"]

GlobalVpnIkePhase2CipherSuiteDefaultDef = Literal["aes128-sha1"]

GlobalVpnIkePhase2CipherSuiteDef = Literal[
    "aes128-cbc-sha1",
    "aes128-cbc-sha256",
    "aes128-gcm",
    "aes128-sha1",
    "aes256-cbc-sha1",
    "aes256-cbc-sha256",
    "aes256-gcm",
]


@dataclass
class OneOfTunnelNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTunnelDescriptionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfListOfIpv4RemotePrivateSubnetsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfLocalPrivateSubnetOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfLocalPrivateSubnetOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class StaticLocalRemotePrivateSubnetDef:
    local_private_subnet: Union[
        OneOfLocalPrivateSubnetOptionsDef1, OneOfLocalPrivateSubnetOptionsDef2
    ] = _field(metadata={"alias": "localPrivateSubnet"})
    remote_private_subnets: OneOfListOfIpv4RemotePrivateSubnetsOptionsDef = _field(
        metadata={"alias": "remotePrivateSubnets"}
    )


@dataclass
class OneOfPresharedSecretOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRemotePublicIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[str, str]]


@dataclass
class OneOfTunnelDnsAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfLocalInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LocalInterfaceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSecondaryRemotePublicIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdIntervalOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdRetriesOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TunnelRedundancyConfigDef:
    secondary_remote_public_ip: OneOfSecondaryRemotePublicIpOptionsDef = _field(
        metadata={"alias": "secondaryRemotePublicIp"}
    )
    dpd_interval: Optional[Union[OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2]] = (
        _field(default=None, metadata={"alias": "dpdInterval"})
    )
    dpd_retries: Optional[Union[OneOfDpdRetriesOptionsDef1, OneOfDpdRetriesOptionsDef2]] = _field(
        default=None, metadata={"alias": "dpdRetries"}
    )


@dataclass
class VpnTunnelInfo:
    """
    Provide specific tunnel information
    """

    local_interface: OneOfLocalInterfaceOptionsDef = _field(metadata={"alias": "localInterface"})
    name: OneOfTunnelNameOptionsDef
    pre_shared_secret: OneOfPresharedSecretOptionsDef = _field(
        metadata={"alias": "preSharedSecret"}
    )
    remote_public_ip: OneOfRemotePublicIpOptionsDef = _field(metadata={"alias": "remotePublicIp"})
    description: Optional[OneOfTunnelDescriptionOptionsDef] = _field(default=None)
    private_subnets: Optional[StaticLocalRemotePrivateSubnetDef] = _field(
        default=None, metadata={"alias": "privateSubnets"}
    )
    tunnel_dns_address: Optional[OneOfTunnelDnsAddressOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelDnsAddress"}
    )
    tunnel_redundancy_configuration: Optional[TunnelRedundancyConfigDef] = _field(
        default=None, metadata={"alias": "tunnelRedundancyConfiguration"}
    )


@dataclass
class OneOfIkePhase1CipherSuiteOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkePhase1CipherSuiteDefaultDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkePhase1CipherSuiteOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkePhase1CipherSuiteDef


@dataclass
class OneOfIkeVersionOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDiffeHellmanGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DiffeHellmanGroupDef


@dataclass
class OneOfDiffeHellmanGroupOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DiffeHellmanGroupDefaultDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRekeyTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRekeyTimerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class IkePhase1:
    """
    IKE Phase 1
    """

    cipher_suite: Union[
        OneOfIkePhase1CipherSuiteOptionsDef1, OneOfIkePhase1CipherSuiteOptionsDef2
    ] = _field(metadata={"alias": "cipherSuite"})
    diffe_hellman_group: Union[
        OneOfDiffeHellmanGroupOptionsDef1, OneOfDiffeHellmanGroupOptionsDef2
    ] = _field(metadata={"alias": "diffeHellmanGroup"})
    ike_version: Optional[OneOfIkeVersionOptionsDef] = _field(
        default=None, metadata={"alias": "ikeVersion"}
    )
    rekey_timer: Optional[Union[OneOfRekeyTimerOptionsDef1, OneOfRekeyTimerOptionsDef2]] = _field(
        default=None, metadata={"alias": "rekeyTimer"}
    )


@dataclass
class OneOfIkePhase2CipherSuiteOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkePhase2CipherSuiteDefaultDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkePhase2CipherSuiteOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkePhase2CipherSuiteDef


@dataclass
class OneOfIkePhase2RekeyTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkePhase2RekeyTimerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class IpSecPolicy:
    """
    Provide IPSEC policy information
    """

    # IKE Phase 1
    ike_phase1: IkePhase1 = _field(metadata={"alias": "ikePhase1"})
    ike_phase2_cipher_suite: Union[
        OneOfIkePhase2CipherSuiteOptionsDef1, OneOfIkePhase2CipherSuiteOptionsDef2
    ] = _field(metadata={"alias": "ikePhase2CipherSuite"})
    ike_phase2_rekey_timer: Optional[
        Union[OneOfIkePhase2RekeyTimerOptionsDef1, OneOfIkePhase2RekeyTimerOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ikePhase2RekeyTimer"})


@dataclass
class VpnTunnels:
    # Provide IPSEC policy information
    ip_sec_policy: IpSecPolicy = _field(metadata={"alias": "ipSecPolicy"})
    # Provide specific tunnel information
    vpn_tunnel_info: VpnTunnelInfo = _field(metadata={"alias": "vpnTunnelInfo"})


@dataclass
class VpnData:
    # Container to provide multiple VPN tunnels configurations
    vpn_tunnels: List[VpnTunnels] = _field(metadata={"alias": "vpnTunnels"})


@dataclass
class Payload:
    """
    AON VPN profile parcel schema for POST request
    """

    data: VpnData
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
    # AON VPN profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListMobilityGlobalVpnPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateVpnProfileParcelForMobilityPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalVpnData:
    # Container to provide multiple VPN tunnels configurations
    vpn_tunnels: List[VpnTunnels] = _field(metadata={"alias": "vpnTunnels"})


@dataclass
class CreateVpnProfileParcelForMobilityPostRequest:
    """
    AON VPN profile parcel schema for POST request
    """

    data: GlobalVpnData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class VpnOneOfTunnelNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfTunnelDescriptionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfListOfIpv4RemotePrivateSubnetsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class VpnOneOfLocalPrivateSubnetOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnStaticLocalRemotePrivateSubnetDef:
    local_private_subnet: Union[
        VpnOneOfLocalPrivateSubnetOptionsDef1, OneOfLocalPrivateSubnetOptionsDef2
    ] = _field(metadata={"alias": "localPrivateSubnet"})
    remote_private_subnets: VpnOneOfListOfIpv4RemotePrivateSubnetsOptionsDef = _field(
        metadata={"alias": "remotePrivateSubnets"}
    )


@dataclass
class VpnOneOfPresharedSecretOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfRemotePublicIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[str, str]]


@dataclass
class VpnOneOfTunnelDnsAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class VpnOneOfLocalInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnLocalInterfaceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfSecondaryRemotePublicIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfDpdIntervalOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfDpdRetriesOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnTunnelRedundancyConfigDef:
    secondary_remote_public_ip: VpnOneOfSecondaryRemotePublicIpOptionsDef = _field(
        metadata={"alias": "secondaryRemotePublicIp"}
    )
    dpd_interval: Optional[
        Union[VpnOneOfDpdIntervalOptionsDef1, VpnOneOfDpdIntervalOptionsDef2]
    ] = _field(default=None, metadata={"alias": "dpdInterval"})
    dpd_retries: Optional[Union[VpnOneOfDpdRetriesOptionsDef1, VpnOneOfDpdRetriesOptionsDef2]] = (
        _field(default=None, metadata={"alias": "dpdRetries"})
    )


@dataclass
class VpnVpnTunnelInfo:
    """
    Provide specific tunnel information
    """

    local_interface: VpnOneOfLocalInterfaceOptionsDef = _field(metadata={"alias": "localInterface"})
    name: VpnOneOfTunnelNameOptionsDef
    pre_shared_secret: VpnOneOfPresharedSecretOptionsDef = _field(
        metadata={"alias": "preSharedSecret"}
    )
    remote_public_ip: VpnOneOfRemotePublicIpOptionsDef = _field(
        metadata={"alias": "remotePublicIp"}
    )
    description: Optional[VpnOneOfTunnelDescriptionOptionsDef] = _field(default=None)
    private_subnets: Optional[VpnStaticLocalRemotePrivateSubnetDef] = _field(
        default=None, metadata={"alias": "privateSubnets"}
    )
    tunnel_dns_address: Optional[VpnOneOfTunnelDnsAddressOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelDnsAddress"}
    )
    tunnel_redundancy_configuration: Optional[VpnTunnelRedundancyConfigDef] = _field(
        default=None, metadata={"alias": "tunnelRedundancyConfiguration"}
    )


@dataclass
class VpnOneOfIkePhase1CipherSuiteOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnIkePhase1CipherSuiteDefaultDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfIkePhase1CipherSuiteOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnIkePhase1CipherSuiteDef


@dataclass
class VpnOneOfIkeVersionOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfDiffeHellmanGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnDiffeHellmanGroupDef


@dataclass
class VpnOneOfDiffeHellmanGroupOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnDiffeHellmanGroupDefaultDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfRekeyTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfRekeyTimerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnIkePhase1:
    """
    IKE Phase 1
    """

    cipher_suite: Union[
        VpnOneOfIkePhase1CipherSuiteOptionsDef1, VpnOneOfIkePhase1CipherSuiteOptionsDef2
    ] = _field(metadata={"alias": "cipherSuite"})
    diffe_hellman_group: Union[
        VpnOneOfDiffeHellmanGroupOptionsDef1, VpnOneOfDiffeHellmanGroupOptionsDef2
    ] = _field(metadata={"alias": "diffeHellmanGroup"})
    ike_version: Optional[VpnOneOfIkeVersionOptionsDef] = _field(
        default=None, metadata={"alias": "ikeVersion"}
    )
    rekey_timer: Optional[Union[VpnOneOfRekeyTimerOptionsDef1, VpnOneOfRekeyTimerOptionsDef2]] = (
        _field(default=None, metadata={"alias": "rekeyTimer"})
    )


@dataclass
class VpnOneOfIkePhase2CipherSuiteOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnIkePhase2CipherSuiteDefaultDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfIkePhase2CipherSuiteOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnIkePhase2CipherSuiteDef


@dataclass
class VpnOneOfIkePhase2RekeyTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfIkePhase2RekeyTimerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnIpSecPolicy:
    """
    Provide IPSEC policy information
    """

    # IKE Phase 1
    ike_phase1: VpnIkePhase1 = _field(metadata={"alias": "ikePhase1"})
    ike_phase2_cipher_suite: Union[
        VpnOneOfIkePhase2CipherSuiteOptionsDef1, VpnOneOfIkePhase2CipherSuiteOptionsDef2
    ] = _field(metadata={"alias": "ikePhase2CipherSuite"})
    ike_phase2_rekey_timer: Optional[
        Union[VpnOneOfIkePhase2RekeyTimerOptionsDef1, VpnOneOfIkePhase2RekeyTimerOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ikePhase2RekeyTimer"})


@dataclass
class VpnVpnTunnels:
    # Provide IPSEC policy information
    ip_sec_policy: VpnIpSecPolicy = _field(metadata={"alias": "ipSecPolicy"})
    # Provide specific tunnel information
    vpn_tunnel_info: VpnVpnTunnelInfo = _field(metadata={"alias": "vpnTunnelInfo"})


@dataclass
class MobilityGlobalVpnData:
    # Container to provide multiple VPN tunnels configurations
    vpn_tunnels: List[VpnVpnTunnels] = _field(metadata={"alias": "vpnTunnels"})


@dataclass
class VpnPayload:
    """
    AON VPN profile parcel schema for PUT request
    """

    data: MobilityGlobalVpnData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleMobilityGlobalVpnPayload:
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
    # AON VPN profile parcel schema for PUT request
    payload: Optional[VpnPayload] = _field(default=None)


@dataclass
class EditVpnProfileParcelForMobilityPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalVpnOneOfTunnelNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalVpnOneOfTunnelDescriptionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalVpnOneOfListOfIpv4RemotePrivateSubnetsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class GlobalVpnOneOfLocalPrivateSubnetOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalVpnStaticLocalRemotePrivateSubnetDef:
    local_private_subnet: Union[
        GlobalVpnOneOfLocalPrivateSubnetOptionsDef1, OneOfLocalPrivateSubnetOptionsDef2
    ] = _field(metadata={"alias": "localPrivateSubnet"})
    remote_private_subnets: GlobalVpnOneOfListOfIpv4RemotePrivateSubnetsOptionsDef = _field(
        metadata={"alias": "remotePrivateSubnets"}
    )


@dataclass
class GlobalVpnOneOfPresharedSecretOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalVpnOneOfRemotePublicIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[str, str]]


@dataclass
class GlobalVpnOneOfTunnelDnsAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class GlobalVpnOneOfLocalInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalVpnLocalInterfaceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalVpnOneOfSecondaryRemotePublicIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalVpnOneOfDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVpnOneOfDpdIntervalOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVpnOneOfDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVpnOneOfDpdRetriesOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVpnTunnelRedundancyConfigDef:
    secondary_remote_public_ip: GlobalVpnOneOfSecondaryRemotePublicIpOptionsDef = _field(
        metadata={"alias": "secondaryRemotePublicIp"}
    )
    dpd_interval: Optional[
        Union[GlobalVpnOneOfDpdIntervalOptionsDef1, GlobalVpnOneOfDpdIntervalOptionsDef2]
    ] = _field(default=None, metadata={"alias": "dpdInterval"})
    dpd_retries: Optional[
        Union[GlobalVpnOneOfDpdRetriesOptionsDef1, GlobalVpnOneOfDpdRetriesOptionsDef2]
    ] = _field(default=None, metadata={"alias": "dpdRetries"})


@dataclass
class GlobalVpnVpnTunnelInfo:
    """
    Provide specific tunnel information
    """

    local_interface: GlobalVpnOneOfLocalInterfaceOptionsDef = _field(
        metadata={"alias": "localInterface"}
    )
    name: GlobalVpnOneOfTunnelNameOptionsDef
    pre_shared_secret: GlobalVpnOneOfPresharedSecretOptionsDef = _field(
        metadata={"alias": "preSharedSecret"}
    )
    remote_public_ip: GlobalVpnOneOfRemotePublicIpOptionsDef = _field(
        metadata={"alias": "remotePublicIp"}
    )
    description: Optional[GlobalVpnOneOfTunnelDescriptionOptionsDef] = _field(default=None)
    private_subnets: Optional[GlobalVpnStaticLocalRemotePrivateSubnetDef] = _field(
        default=None, metadata={"alias": "privateSubnets"}
    )
    tunnel_dns_address: Optional[GlobalVpnOneOfTunnelDnsAddressOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelDnsAddress"}
    )
    tunnel_redundancy_configuration: Optional[GlobalVpnTunnelRedundancyConfigDef] = _field(
        default=None, metadata={"alias": "tunnelRedundancyConfiguration"}
    )


@dataclass
class GlobalVpnOneOfIkePhase1CipherSuiteOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalVpnIkePhase1CipherSuiteDefaultDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalVpnOneOfIkePhase1CipherSuiteOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalVpnIkePhase1CipherSuiteDef


@dataclass
class GlobalVpnOneOfIkeVersionOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVpnOneOfDiffeHellmanGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalVpnDiffeHellmanGroupDef


@dataclass
class GlobalVpnOneOfDiffeHellmanGroupOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalVpnDiffeHellmanGroupDefaultDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalVpnOneOfRekeyTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVpnOneOfRekeyTimerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVpnIkePhase1:
    """
    IKE Phase 1
    """

    cipher_suite: Union[
        GlobalVpnOneOfIkePhase1CipherSuiteOptionsDef1, GlobalVpnOneOfIkePhase1CipherSuiteOptionsDef2
    ] = _field(metadata={"alias": "cipherSuite"})
    diffe_hellman_group: Union[
        GlobalVpnOneOfDiffeHellmanGroupOptionsDef1, GlobalVpnOneOfDiffeHellmanGroupOptionsDef2
    ] = _field(metadata={"alias": "diffeHellmanGroup"})
    ike_version: Optional[GlobalVpnOneOfIkeVersionOptionsDef] = _field(
        default=None, metadata={"alias": "ikeVersion"}
    )
    rekey_timer: Optional[
        Union[GlobalVpnOneOfRekeyTimerOptionsDef1, GlobalVpnOneOfRekeyTimerOptionsDef2]
    ] = _field(default=None, metadata={"alias": "rekeyTimer"})


@dataclass
class GlobalVpnOneOfIkePhase2CipherSuiteOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalVpnIkePhase2CipherSuiteDefaultDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalVpnOneOfIkePhase2CipherSuiteOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalVpnIkePhase2CipherSuiteDef


@dataclass
class GlobalVpnOneOfIkePhase2RekeyTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVpnOneOfIkePhase2RekeyTimerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVpnIpSecPolicy:
    """
    Provide IPSEC policy information
    """

    # IKE Phase 1
    ike_phase1: GlobalVpnIkePhase1 = _field(metadata={"alias": "ikePhase1"})
    ike_phase2_cipher_suite: Union[
        GlobalVpnOneOfIkePhase2CipherSuiteOptionsDef1, GlobalVpnOneOfIkePhase2CipherSuiteOptionsDef2
    ] = _field(metadata={"alias": "ikePhase2CipherSuite"})
    ike_phase2_rekey_timer: Optional[
        Union[
            GlobalVpnOneOfIkePhase2RekeyTimerOptionsDef1,
            GlobalVpnOneOfIkePhase2RekeyTimerOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ikePhase2RekeyTimer"})


@dataclass
class GlobalVpnVpnTunnels:
    # Provide IPSEC policy information
    ip_sec_policy: GlobalVpnIpSecPolicy = _field(metadata={"alias": "ipSecPolicy"})
    # Provide specific tunnel information
    vpn_tunnel_info: GlobalVpnVpnTunnelInfo = _field(metadata={"alias": "vpnTunnelInfo"})


@dataclass
class FeatureProfileMobilityGlobalVpnData:
    # Container to provide multiple VPN tunnels configurations
    vpn_tunnels: List[GlobalVpnVpnTunnels] = _field(metadata={"alias": "vpnTunnels"})


@dataclass
class EditVpnProfileParcelForMobilityPutRequest:
    """
    AON VPN profile parcel schema for PUT request
    """

    data: FeatureProfileMobilityGlobalVpnData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
