# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

InterfaceModeDef = Literal["access", "trunk"]

DefaultOptionTypeDef = Literal["default"]

InterfaceSpeedDef = Literal["10", "100", "1000", "10000", "2500", "25000"]

InterfaceDuplexDef = Literal["full", "half"]

InterfacePortControlDef = Literal["auto", "force-authorized", "force-unauthorized"]

InterfaceHostModeDef = Literal["multi-auth", "multi-domain", "multi-host", "single-host"]

InterfaceControlDirectionDef = Literal["both", "in"]

SwitchportInterfaceModeDef = Literal["access", "trunk"]

SwitchportInterfaceSpeedDef = Literal["10", "100", "1000", "10000", "2500", "25000"]

SwitchportInterfaceDuplexDef = Literal["full", "half"]

SwitchportInterfacePortControlDef = Literal["auto", "force-authorized", "force-unauthorized"]

SwitchportInterfaceHostModeDef = Literal["multi-auth", "multi-domain", "multi-host", "single-host"]

SwitchportInterfaceControlDirectionDef = Literal["both", "in"]

ServiceSwitchportInterfaceModeDef = Literal["access", "trunk"]

ServiceSwitchportInterfaceSpeedDef = Literal["10", "100", "1000", "10000", "2500", "25000"]

ServiceSwitchportInterfaceDuplexDef = Literal["full", "half"]

ServiceSwitchportInterfacePortControlDef = Literal["auto", "force-authorized", "force-unauthorized"]

ServiceSwitchportInterfaceHostModeDef = Literal[
    "multi-auth", "multi-domain", "multi-host", "single-host"
]

ServiceSwitchportInterfaceControlDirectionDef = Literal["both", "in"]


@dataclass
class OneOfInterfaceIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceIfNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceShutdownOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceShutdownOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceShutdownOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceSpeedOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceSpeedDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceSpeedOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceSpeedOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceDuplexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceDuplexDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceDuplexOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDuplexOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceSwitchportAccessVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceSwitchportAccessVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceSwitchportAccessVlanOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceVlansOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceVlansOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceVlansOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceSwitchportTrunkNativeVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceSwitchportTrunkNativeVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceSwitchportTrunkNativeVlanOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfOnBooleanDefaultFalseNoVariableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultFalseNoVariableOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfacePortControlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfacePortControlDef


@dataclass
class OneOfInterfacePortControlOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfacePortControlOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceVoiceVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceVoiceVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceVoiceVlanOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfacePaeEnableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfacePaeEnableOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfacePaeEnableOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceMacAuthenticationBypassOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceMacAuthenticationBypassOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceMacAuthenticationBypassOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceHostModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceHostModeDef


@dataclass
class OneOfInterfaceHostModeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceHostModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceEnablePeriodicReauthOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceEnablePeriodicReauthOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceEnablePeriodicReauthOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceInactivityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceInactivityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceInactivityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceReauthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceReauthenticationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceReauthenticationOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceControlDirectionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceControlDirectionDef


@dataclass
class OneOfInterfaceControlDirectionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceControlDirectionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceRestrictedVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceRestrictedVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceRestrictedVlanOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceGuestVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceGuestVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceGuestVlanOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceCriticalVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceCriticalVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceCriticalVlanOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceEnableVoiceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceEnableVoiceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceEnableVoiceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Interface:
    if_name: Union[OneOfInterfaceIfNameOptionsDef1, OneOfInterfaceIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    control_direction: Optional[
        Union[
            OneOfInterfaceControlDirectionOptionsDef1,
            OneOfInterfaceControlDirectionOptionsDef2,
            OneOfInterfaceControlDirectionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controlDirection"})
    critical_vlan: Optional[
        Union[
            OneOfInterfaceCriticalVlanOptionsDef1,
            OneOfInterfaceCriticalVlanOptionsDef2,
            OneOfInterfaceCriticalVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "criticalVlan"})
    duplex: Optional[
        Union[
            OneOfInterfaceDuplexOptionsDef1,
            OneOfInterfaceDuplexOptionsDef2,
            OneOfInterfaceDuplexOptionsDef3,
        ]
    ] = _field(default=None)
    enable_dot1x: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDot1x"})
    enable_periodic_reauth: Optional[
        Union[
            OneOfInterfaceEnablePeriodicReauthOptionsDef1,
            OneOfInterfaceEnablePeriodicReauthOptionsDef2,
            OneOfInterfaceEnablePeriodicReauthOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "enablePeriodicReauth"})
    enable_voice: Optional[
        Union[
            OneOfInterfaceEnableVoiceOptionsDef1,
            OneOfInterfaceEnableVoiceOptionsDef2,
            OneOfInterfaceEnableVoiceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "enableVoice"})
    guest_vlan: Optional[
        Union[
            OneOfInterfaceGuestVlanOptionsDef1,
            OneOfInterfaceGuestVlanOptionsDef2,
            OneOfInterfaceGuestVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "guestVlan"})
    host_mode: Optional[
        Union[
            OneOfInterfaceHostModeOptionsDef1,
            OneOfInterfaceHostModeOptionsDef2,
            OneOfInterfaceHostModeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "hostMode"})
    inactivity: Optional[
        Union[
            OneOfInterfaceInactivityOptionsDef1,
            OneOfInterfaceInactivityOptionsDef2,
            OneOfInterfaceInactivityOptionsDef3,
        ]
    ] = _field(default=None)
    mac_authentication_bypass: Optional[
        Union[
            OneOfInterfaceMacAuthenticationBypassOptionsDef1,
            OneOfInterfaceMacAuthenticationBypassOptionsDef2,
            OneOfInterfaceMacAuthenticationBypassOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "macAuthenticationBypass"})
    mode: Optional[OneOfInterfaceModeOptionsDef] = _field(default=None)
    pae_enable: Optional[
        Union[
            OneOfInterfacePaeEnableOptionsDef1,
            OneOfInterfacePaeEnableOptionsDef2,
            OneOfInterfacePaeEnableOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "paeEnable"})
    port_control: Optional[
        Union[
            OneOfInterfacePortControlOptionsDef1,
            OneOfInterfacePortControlOptionsDef2,
            OneOfInterfacePortControlOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "portControl"})
    reauthentication: Optional[
        Union[
            OneOfInterfaceReauthenticationOptionsDef1,
            OneOfInterfaceReauthenticationOptionsDef2,
            OneOfInterfaceReauthenticationOptionsDef3,
        ]
    ] = _field(default=None)
    restricted_vlan: Optional[
        Union[
            OneOfInterfaceRestrictedVlanOptionsDef1,
            OneOfInterfaceRestrictedVlanOptionsDef2,
            OneOfInterfaceRestrictedVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "restrictedVlan"})
    shutdown: Optional[
        Union[
            OneOfInterfaceShutdownOptionsDef1,
            OneOfInterfaceShutdownOptionsDef2,
            OneOfInterfaceShutdownOptionsDef3,
        ]
    ] = _field(default=None)
    speed: Optional[
        Union[
            OneOfInterfaceSpeedOptionsDef1,
            OneOfInterfaceSpeedOptionsDef2,
            OneOfInterfaceSpeedOptionsDef3,
        ]
    ] = _field(default=None)
    switchport_access_vlan: Optional[
        Union[
            OneOfInterfaceSwitchportAccessVlanOptionsDef1,
            OneOfInterfaceSwitchportAccessVlanOptionsDef2,
            OneOfInterfaceSwitchportAccessVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "switchportAccessVlan"})
    switchport_trunk_allowed_vlans: Optional[
        Union[
            OneOfInterfaceVlansOptionsDef1,
            OneOfInterfaceVlansOptionsDef2,
            OneOfInterfaceVlansOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "switchportTrunkAllowedVlans"})
    switchport_trunk_native_vlan: Optional[
        Union[
            OneOfInterfaceSwitchportTrunkNativeVlanOptionsDef1,
            OneOfInterfaceSwitchportTrunkNativeVlanOptionsDef2,
            OneOfInterfaceSwitchportTrunkNativeVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "switchportTrunkNativeVlan"})
    voice_vlan: Optional[
        Union[
            OneOfInterfaceVoiceVlanOptionsDef1,
            OneOfInterfaceVoiceVlanOptionsDef2,
            OneOfInterfaceVoiceVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "voiceVlan"})


@dataclass
class OneOfAgeTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAgeTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAgeTimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfStaticMacAddressMacaddrOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfStaticMacAddressMacaddrOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticMacAddressVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfStaticMacAddressVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticMacAddressIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfStaticMacAddressIfNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class StaticMacAddress:
    macaddr: Union[OneOfStaticMacAddressMacaddrOptionsDef1, OneOfStaticMacAddressMacaddrOptionsDef2]
    vlan: Union[OneOfStaticMacAddressVlanOptionsDef1, OneOfStaticMacAddressVlanOptionsDef2]
    if_name: Optional[
        Union[OneOfStaticMacAddressIfNameOptionsDef1, OneOfStaticMacAddressIfNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ifName"})


@dataclass
class SwitchportData:
    age_time: Optional[
        Union[OneOfAgeTimeOptionsDef1, OneOfAgeTimeOptionsDef2, OneOfAgeTimeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ageTime"})
    # Interface name: GigabitEthernet0/<>/<> when present
    interface: Optional[List[Interface]] = _field(default=None)
    # Add static MAC address entries for interface
    static_mac_address: Optional[List[StaticMacAddress]] = _field(
        default=None, metadata={"alias": "staticMacAddress"}
    )


@dataclass
class Payload:
    """
    SwitchPort profile parcel schema for POST request
    """

    data: SwitchportData
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
    # SwitchPort profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanServiceSwitchportPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CedgeServiceProfileSwitchportParcelRestfulResourcePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceSwitchportData:
    age_time: Optional[
        Union[OneOfAgeTimeOptionsDef1, OneOfAgeTimeOptionsDef2, OneOfAgeTimeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ageTime"})
    # Interface name: GigabitEthernet0/<>/<> when present
    interface: Optional[List[Interface]] = _field(default=None)
    # Add static MAC address entries for interface
    static_mac_address: Optional[List[StaticMacAddress]] = _field(
        default=None, metadata={"alias": "staticMacAddress"}
    )


@dataclass
class CedgeServiceProfileSwitchportParcelRestfulResourcePostRequest:
    """
    SwitchPort profile parcel schema for POST request
    """

    data: ServiceSwitchportData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class SwitchportOneOfInterfaceIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SwitchportOneOfInterfaceModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SwitchportInterfaceModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SwitchportOneOfInterfaceSpeedOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SwitchportInterfaceSpeedDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SwitchportOneOfInterfaceDuplexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SwitchportInterfaceDuplexDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SwitchportOneOfInterfaceSwitchportAccessVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfInterfaceVlansOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SwitchportOneOfInterfaceSwitchportTrunkNativeVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfInterfacePortControlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SwitchportInterfacePortControlDef


@dataclass
class SwitchportOneOfInterfaceVoiceVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfInterfaceHostModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SwitchportInterfaceHostModeDef


@dataclass
class SwitchportOneOfInterfaceInactivityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfInterfaceReauthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfInterfaceReauthenticationOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfInterfaceControlDirectionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SwitchportInterfaceControlDirectionDef


@dataclass
class SwitchportOneOfInterfaceRestrictedVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfInterfaceGuestVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfInterfaceCriticalVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportInterface:
    if_name: Union[SwitchportOneOfInterfaceIfNameOptionsDef1, OneOfInterfaceIfNameOptionsDef2] = (
        _field(metadata={"alias": "ifName"})
    )
    control_direction: Optional[
        Union[
            SwitchportOneOfInterfaceControlDirectionOptionsDef1,
            OneOfInterfaceControlDirectionOptionsDef2,
            OneOfInterfaceControlDirectionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controlDirection"})
    critical_vlan: Optional[
        Union[
            SwitchportOneOfInterfaceCriticalVlanOptionsDef1,
            OneOfInterfaceCriticalVlanOptionsDef2,
            OneOfInterfaceCriticalVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "criticalVlan"})
    duplex: Optional[
        Union[
            SwitchportOneOfInterfaceDuplexOptionsDef1,
            OneOfInterfaceDuplexOptionsDef2,
            OneOfInterfaceDuplexOptionsDef3,
        ]
    ] = _field(default=None)
    enable_dot1x: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDot1x"})
    enable_periodic_reauth: Optional[
        Union[
            OneOfInterfaceEnablePeriodicReauthOptionsDef1,
            OneOfInterfaceEnablePeriodicReauthOptionsDef2,
            OneOfInterfaceEnablePeriodicReauthOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "enablePeriodicReauth"})
    enable_voice: Optional[
        Union[
            OneOfInterfaceEnableVoiceOptionsDef1,
            OneOfInterfaceEnableVoiceOptionsDef2,
            OneOfInterfaceEnableVoiceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "enableVoice"})
    guest_vlan: Optional[
        Union[
            SwitchportOneOfInterfaceGuestVlanOptionsDef1,
            OneOfInterfaceGuestVlanOptionsDef2,
            OneOfInterfaceGuestVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "guestVlan"})
    host_mode: Optional[
        Union[
            SwitchportOneOfInterfaceHostModeOptionsDef1,
            OneOfInterfaceHostModeOptionsDef2,
            OneOfInterfaceHostModeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "hostMode"})
    inactivity: Optional[
        Union[
            SwitchportOneOfInterfaceInactivityOptionsDef1,
            OneOfInterfaceInactivityOptionsDef2,
            OneOfInterfaceInactivityOptionsDef3,
        ]
    ] = _field(default=None)
    mac_authentication_bypass: Optional[
        Union[
            OneOfInterfaceMacAuthenticationBypassOptionsDef1,
            OneOfInterfaceMacAuthenticationBypassOptionsDef2,
            OneOfInterfaceMacAuthenticationBypassOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "macAuthenticationBypass"})
    mode: Optional[SwitchportOneOfInterfaceModeOptionsDef] = _field(default=None)
    pae_enable: Optional[
        Union[
            OneOfInterfacePaeEnableOptionsDef1,
            OneOfInterfacePaeEnableOptionsDef2,
            OneOfInterfacePaeEnableOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "paeEnable"})
    port_control: Optional[
        Union[
            SwitchportOneOfInterfacePortControlOptionsDef1,
            OneOfInterfacePortControlOptionsDef2,
            OneOfInterfacePortControlOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "portControl"})
    reauthentication: Optional[
        Union[
            SwitchportOneOfInterfaceReauthenticationOptionsDef1,
            OneOfInterfaceReauthenticationOptionsDef2,
            SwitchportOneOfInterfaceReauthenticationOptionsDef3,
        ]
    ] = _field(default=None)
    restricted_vlan: Optional[
        Union[
            SwitchportOneOfInterfaceRestrictedVlanOptionsDef1,
            OneOfInterfaceRestrictedVlanOptionsDef2,
            OneOfInterfaceRestrictedVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "restrictedVlan"})
    shutdown: Optional[
        Union[
            OneOfInterfaceShutdownOptionsDef1,
            OneOfInterfaceShutdownOptionsDef2,
            OneOfInterfaceShutdownOptionsDef3,
        ]
    ] = _field(default=None)
    speed: Optional[
        Union[
            SwitchportOneOfInterfaceSpeedOptionsDef1,
            OneOfInterfaceSpeedOptionsDef2,
            OneOfInterfaceSpeedOptionsDef3,
        ]
    ] = _field(default=None)
    switchport_access_vlan: Optional[
        Union[
            SwitchportOneOfInterfaceSwitchportAccessVlanOptionsDef1,
            OneOfInterfaceSwitchportAccessVlanOptionsDef2,
            OneOfInterfaceSwitchportAccessVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "switchportAccessVlan"})
    switchport_trunk_allowed_vlans: Optional[
        Union[
            SwitchportOneOfInterfaceVlansOptionsDef1,
            OneOfInterfaceVlansOptionsDef2,
            OneOfInterfaceVlansOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "switchportTrunkAllowedVlans"})
    switchport_trunk_native_vlan: Optional[
        Union[
            SwitchportOneOfInterfaceSwitchportTrunkNativeVlanOptionsDef1,
            OneOfInterfaceSwitchportTrunkNativeVlanOptionsDef2,
            OneOfInterfaceSwitchportTrunkNativeVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "switchportTrunkNativeVlan"})
    voice_vlan: Optional[
        Union[
            SwitchportOneOfInterfaceVoiceVlanOptionsDef1,
            OneOfInterfaceVoiceVlanOptionsDef2,
            OneOfInterfaceVoiceVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "voiceVlan"})


@dataclass
class SwitchportOneOfAgeTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfAgeTimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfStaticMacAddressMacaddrOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SwitchportOneOfStaticMacAddressVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchportOneOfStaticMacAddressIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SwitchportStaticMacAddress:
    macaddr: Union[
        SwitchportOneOfStaticMacAddressMacaddrOptionsDef1, OneOfStaticMacAddressMacaddrOptionsDef2
    ]
    vlan: Union[
        SwitchportOneOfStaticMacAddressVlanOptionsDef1, OneOfStaticMacAddressVlanOptionsDef2
    ]
    if_name: Optional[
        Union[
            SwitchportOneOfStaticMacAddressIfNameOptionsDef1, OneOfStaticMacAddressIfNameOptionsDef2
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})


@dataclass
class SdwanServiceSwitchportData:
    age_time: Optional[
        Union[
            SwitchportOneOfAgeTimeOptionsDef1,
            OneOfAgeTimeOptionsDef2,
            SwitchportOneOfAgeTimeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ageTime"})
    # Interface name: GigabitEthernet0/<>/<> when present
    interface: Optional[List[SwitchportInterface]] = _field(default=None)
    # Add static MAC address entries for interface
    static_mac_address: Optional[List[SwitchportStaticMacAddress]] = _field(
        default=None, metadata={"alias": "staticMacAddress"}
    )


@dataclass
class SwitchportPayload:
    """
    SwitchPort profile parcel schema for PUT request
    """

    data: SdwanServiceSwitchportData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanServiceSwitchportPayload:
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
    # SwitchPort profile parcel schema for PUT request
    payload: Optional[SwitchportPayload] = _field(default=None)


@dataclass
class EditSwitchportParcelAssociationForServicePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceSwitchportOneOfInterfaceIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceSwitchportOneOfInterfaceModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceSwitchportInterfaceModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceSwitchportOneOfInterfaceSpeedOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceSwitchportInterfaceSpeedDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceSwitchportOneOfInterfaceDuplexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceSwitchportInterfaceDuplexDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceSwitchportOneOfInterfaceSwitchportAccessVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfInterfaceVlansOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceSwitchportOneOfInterfaceSwitchportTrunkNativeVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfInterfacePortControlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceSwitchportInterfacePortControlDef


@dataclass
class ServiceSwitchportOneOfInterfaceVoiceVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfInterfaceHostModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceSwitchportInterfaceHostModeDef


@dataclass
class ServiceSwitchportOneOfInterfaceInactivityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfInterfaceReauthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfInterfaceReauthenticationOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfInterfaceControlDirectionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceSwitchportInterfaceControlDirectionDef


@dataclass
class ServiceSwitchportOneOfInterfaceRestrictedVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfInterfaceGuestVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfInterfaceCriticalVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportInterface:
    if_name: Union[
        ServiceSwitchportOneOfInterfaceIfNameOptionsDef1, OneOfInterfaceIfNameOptionsDef2
    ] = _field(metadata={"alias": "ifName"})
    control_direction: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceControlDirectionOptionsDef1,
            OneOfInterfaceControlDirectionOptionsDef2,
            OneOfInterfaceControlDirectionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controlDirection"})
    critical_vlan: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceCriticalVlanOptionsDef1,
            OneOfInterfaceCriticalVlanOptionsDef2,
            OneOfInterfaceCriticalVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "criticalVlan"})
    duplex: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceDuplexOptionsDef1,
            OneOfInterfaceDuplexOptionsDef2,
            OneOfInterfaceDuplexOptionsDef3,
        ]
    ] = _field(default=None)
    enable_dot1x: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDot1x"})
    enable_periodic_reauth: Optional[
        Union[
            OneOfInterfaceEnablePeriodicReauthOptionsDef1,
            OneOfInterfaceEnablePeriodicReauthOptionsDef2,
            OneOfInterfaceEnablePeriodicReauthOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "enablePeriodicReauth"})
    enable_voice: Optional[
        Union[
            OneOfInterfaceEnableVoiceOptionsDef1,
            OneOfInterfaceEnableVoiceOptionsDef2,
            OneOfInterfaceEnableVoiceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "enableVoice"})
    guest_vlan: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceGuestVlanOptionsDef1,
            OneOfInterfaceGuestVlanOptionsDef2,
            OneOfInterfaceGuestVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "guestVlan"})
    host_mode: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceHostModeOptionsDef1,
            OneOfInterfaceHostModeOptionsDef2,
            OneOfInterfaceHostModeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "hostMode"})
    inactivity: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceInactivityOptionsDef1,
            OneOfInterfaceInactivityOptionsDef2,
            OneOfInterfaceInactivityOptionsDef3,
        ]
    ] = _field(default=None)
    mac_authentication_bypass: Optional[
        Union[
            OneOfInterfaceMacAuthenticationBypassOptionsDef1,
            OneOfInterfaceMacAuthenticationBypassOptionsDef2,
            OneOfInterfaceMacAuthenticationBypassOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "macAuthenticationBypass"})
    mode: Optional[ServiceSwitchportOneOfInterfaceModeOptionsDef] = _field(default=None)
    pae_enable: Optional[
        Union[
            OneOfInterfacePaeEnableOptionsDef1,
            OneOfInterfacePaeEnableOptionsDef2,
            OneOfInterfacePaeEnableOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "paeEnable"})
    port_control: Optional[
        Union[
            ServiceSwitchportOneOfInterfacePortControlOptionsDef1,
            OneOfInterfacePortControlOptionsDef2,
            OneOfInterfacePortControlOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "portControl"})
    reauthentication: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceReauthenticationOptionsDef1,
            OneOfInterfaceReauthenticationOptionsDef2,
            ServiceSwitchportOneOfInterfaceReauthenticationOptionsDef3,
        ]
    ] = _field(default=None)
    restricted_vlan: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceRestrictedVlanOptionsDef1,
            OneOfInterfaceRestrictedVlanOptionsDef2,
            OneOfInterfaceRestrictedVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "restrictedVlan"})
    shutdown: Optional[
        Union[
            OneOfInterfaceShutdownOptionsDef1,
            OneOfInterfaceShutdownOptionsDef2,
            OneOfInterfaceShutdownOptionsDef3,
        ]
    ] = _field(default=None)
    speed: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceSpeedOptionsDef1,
            OneOfInterfaceSpeedOptionsDef2,
            OneOfInterfaceSpeedOptionsDef3,
        ]
    ] = _field(default=None)
    switchport_access_vlan: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceSwitchportAccessVlanOptionsDef1,
            OneOfInterfaceSwitchportAccessVlanOptionsDef2,
            OneOfInterfaceSwitchportAccessVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "switchportAccessVlan"})
    switchport_trunk_allowed_vlans: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceVlansOptionsDef1,
            OneOfInterfaceVlansOptionsDef2,
            OneOfInterfaceVlansOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "switchportTrunkAllowedVlans"})
    switchport_trunk_native_vlan: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceSwitchportTrunkNativeVlanOptionsDef1,
            OneOfInterfaceSwitchportTrunkNativeVlanOptionsDef2,
            OneOfInterfaceSwitchportTrunkNativeVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "switchportTrunkNativeVlan"})
    voice_vlan: Optional[
        Union[
            ServiceSwitchportOneOfInterfaceVoiceVlanOptionsDef1,
            OneOfInterfaceVoiceVlanOptionsDef2,
            OneOfInterfaceVoiceVlanOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "voiceVlan"})


@dataclass
class ServiceSwitchportOneOfAgeTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfAgeTimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfStaticMacAddressMacaddrOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceSwitchportOneOfStaticMacAddressVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceSwitchportOneOfStaticMacAddressIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceSwitchportStaticMacAddress:
    macaddr: Union[
        ServiceSwitchportOneOfStaticMacAddressMacaddrOptionsDef1,
        OneOfStaticMacAddressMacaddrOptionsDef2,
    ]
    vlan: Union[
        ServiceSwitchportOneOfStaticMacAddressVlanOptionsDef1, OneOfStaticMacAddressVlanOptionsDef2
    ]
    if_name: Optional[
        Union[
            ServiceSwitchportOneOfStaticMacAddressIfNameOptionsDef1,
            OneOfStaticMacAddressIfNameOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})


@dataclass
class FeatureProfileSdwanServiceSwitchportData:
    age_time: Optional[
        Union[
            ServiceSwitchportOneOfAgeTimeOptionsDef1,
            OneOfAgeTimeOptionsDef2,
            ServiceSwitchportOneOfAgeTimeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ageTime"})
    # Interface name: GigabitEthernet0/<>/<> when present
    interface: Optional[List[ServiceSwitchportInterface]] = _field(default=None)
    # Add static MAC address entries for interface
    static_mac_address: Optional[List[ServiceSwitchportStaticMacAddress]] = _field(
        default=None, metadata={"alias": "staticMacAddress"}
    )


@dataclass
class EditSwitchportParcelAssociationForServicePutRequest:
    """
    SwitchPort profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanServiceSwitchportData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
