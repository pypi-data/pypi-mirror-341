# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

AclTypeDef = Literal["extended", "standard"]

DefaultActionDef = Literal["accept", "drop"]

DefaultOptionTypeDef = Literal["default"]

Value = Literal["drop"]

VariableOptionTypeDef = Literal["variable"]

SequencesActionTypeDef = Literal["accept", "drop"]

Ipv4AclValue = Literal["accept"]

SequencesMatchEntriesTcpPortEqAppNamesDef = Literal[
    "bgp",
    "chargen",
    "cmd",
    "daytime",
    "discard",
    "domain",
    "echo",
    "exec",
    "finger",
    "ftp",
    "ftp-data",
    "gopher",
    "hostname",
    "ident",
    "irc",
    "klogin",
    "kshell",
    "login",
    "lpd",
    "msrpc",
    "nntp",
    "onep-plain",
    "onep-tls",
    "pim-auto-rp",
    "pop2",
    "pop3",
    "smtp",
    "sunrpc",
    "syslog",
    "tacacs",
    "talk",
    "telnet",
    "time",
    "uucp",
    "whois",
    "www",
]

SequencesMatchEntriesUdpPortEqAppNamesDef = Literal[
    "biff",
    "bootpc",
    "bootps",
    "discard",
    "dnsix",
    "domain",
    "echo",
    "isakmp",
    "mobile-ip",
    "nameserver",
    "netbios-dgm",
    "netbios-ns",
    "netbios-ss",
    "non500-isakmp",
    "ntp",
    "pim-auto-rp",
    "rip",
    "ripv6",
    "snmp",
    "snmptrap",
    "sunrpc",
    "syslog",
    "tacacs",
    "talk",
    "tftp",
    "time",
    "who",
    "xdmcp",
]

SequencesMatchEntriesPortOperatorDef = Literal["eq", "gt", "lt", "range"]

SequencesMatchEntriesTcpBitDef = Literal["ack", "fin", "psh", "rst", "syn", "urg"]


@dataclass
class OneOfAclTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AclTypeDef


@dataclass
class OneOfDefaultActionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultActionDef


@dataclass
class OneOfDefaultActionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSequencesSequenceNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSequencesMatchEntriesSourceTypeHostOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfSequencesMatchEntriesSourceHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfSequencesMatchEntriesSourceHostOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SourceAddress1:
    source_host: Union[
        OneOfSequencesMatchEntriesSourceHostOptionsDef1,
        OneOfSequencesMatchEntriesSourceHostOptionsDef2,
    ] = _field(metadata={"alias": "sourceHost"})
    source_type: OneOfSequencesMatchEntriesSourceTypeHostOptionsDef = _field(
        metadata={"alias": "sourceType"}
    )


@dataclass
class OneOfSequencesMatchEntriesSourceTypeIpPrefixOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfSequencesMatchEntriesSourceIpPrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSequencesMatchEntriesSourceIpPrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SourceAddress2:
    source_ip_prefix: Union[
        OneOfSequencesMatchEntriesSourceIpPrefixOptionsDef1,
        OneOfSequencesMatchEntriesSourceIpPrefixOptionsDef2,
    ] = _field(metadata={"alias": "sourceIpPrefix"})
    source_type: OneOfSequencesMatchEntriesSourceTypeIpPrefixOptionsDef = _field(
        metadata={"alias": "sourceType"}
    )


@dataclass
class MatchEntries:
    """
    Define match conditions
    """

    # Source Address
    source_address: Union[SourceAddress1, SourceAddress2] = _field(
        metadata={"alias": "sourceAddress"}
    )


@dataclass
class OneOfSequencesActionTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SequencesActionTypeDef


@dataclass
class OneOfSequencesActionTypeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4AclValue  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSequencesActionsLogOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Actions:
    """
    Actions
    """

    log: OneOfSequencesActionsLogOptionsDef


@dataclass
class StandardAclSequences:
    action_type: Union[OneOfSequencesActionTypeOptionsDef1, OneOfSequencesActionTypeOptionsDef2] = (
        _field(metadata={"alias": "actionType"})
    )
    sequence_name: OneOfSequencesSequenceNameOptionsDef = _field(metadata={"alias": "sequenceName"})
    # Actions
    actions: Optional[Actions] = _field(default=None)
    # Define match conditions
    match_entries: Optional[MatchEntries] = _field(default=None, metadata={"alias": "matchEntries"})


@dataclass
class Actions1:
    log: OneOfSequencesActionsLogOptionsDef


@dataclass
class OneOfSequencesActionsLogInputOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Actions2:
    log_input: OneOfSequencesActionsLogInputOptionsDef = _field(metadata={"alias": "logInput"})


@dataclass
class ExtendedAclSequences1:
    action_type: Union[OneOfSequencesActionTypeOptionsDef1, OneOfSequencesActionTypeOptionsDef2] = (
        _field(metadata={"alias": "actionType"})
    )
    # Actions
    actions: Union[Actions1, Actions2]
    match_entries: Any = _field(metadata={"alias": "matchEntries"})
    sequence_name: OneOfSequencesSequenceNameOptionsDef = _field(metadata={"alias": "sequenceName"})


@dataclass
class Protocol:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfSequencesMatchEntriesSourceAddressOptionsDef1:
    source_host: Union[
        OneOfSequencesMatchEntriesSourceHostOptionsDef1,
        OneOfSequencesMatchEntriesSourceHostOptionsDef2,
    ] = _field(metadata={"alias": "sourceHost"})
    source_type: OneOfSequencesMatchEntriesSourceTypeHostOptionsDef = _field(
        metadata={"alias": "sourceType"}
    )


@dataclass
class OneOfSequencesMatchEntriesSourceAddressOptionsDef2:
    source_ip_prefix: Union[
        OneOfSequencesMatchEntriesSourceIpPrefixOptionsDef1,
        OneOfSequencesMatchEntriesSourceIpPrefixOptionsDef2,
    ] = _field(metadata={"alias": "sourceIpPrefix"})
    source_type: OneOfSequencesMatchEntriesSourceTypeIpPrefixOptionsDef = _field(
        metadata={"alias": "sourceType"}
    )


@dataclass
class OneOfSequencesMatchEntriesSourceTypeObjectGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ParcelReferenceDef:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfSequencesMatchEntriesSourceAddressOptionsDef3:
    source_network_object_group: ParcelReferenceDef = _field(
        metadata={"alias": "sourceNetworkObjectGroup"}
    )
    source_type: OneOfSequencesMatchEntriesSourceTypeObjectGroupOptionsDef = _field(
        metadata={"alias": "sourceType"}
    )


@dataclass
class Operator:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfSequencesMatchEntriesPortLtValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesMatchEntriesPortLtValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSequencesMatchEntriesPortGtValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesMatchEntriesPortGtValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSequencesMatchEntriesPortEqNumbersOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfSequencesMatchEntriesPortEqNumbersOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSequencesMatchEntriesTcpPortEqAppNamesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[
        SequencesMatchEntriesTcpPortEqAppNamesDef
    ]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSequencesMatchEntriesTcpPortEqAppNamesOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class TcpEqValue1:
    port_numbers: Union[
        OneOfSequencesMatchEntriesPortEqNumbersOptionsDef1,
        OneOfSequencesMatchEntriesPortEqNumbersOptionsDef2,
    ] = _field(metadata={"alias": "portNumbers"})
    app_names: Optional[
        Union[
            OneOfSequencesMatchEntriesTcpPortEqAppNamesOptionsDef1,
            OneOfSequencesMatchEntriesTcpPortEqAppNamesOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "appNames"})


@dataclass
class TcpEqValue2:
    app_names: Union[
        OneOfSequencesMatchEntriesTcpPortEqAppNamesOptionsDef1,
        OneOfSequencesMatchEntriesTcpPortEqAppNamesOptionsDef2,
    ] = _field(metadata={"alias": "appNames"})
    port_numbers: Optional[
        Union[
            OneOfSequencesMatchEntriesPortEqNumbersOptionsDef1,
            OneOfSequencesMatchEntriesPortEqNumbersOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "portNumbers"})


@dataclass
class EqValue1:
    # Match Source TCP Ports That is Equal to Any Value in This List
    tcp_eq_value: Union[TcpEqValue1, TcpEqValue2] = _field(metadata={"alias": "tcpEqValue"})


@dataclass
class OneOfSequencesMatchEntriesUdpPortEqAppNamesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[
        SequencesMatchEntriesUdpPortEqAppNamesDef
    ]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSequencesMatchEntriesUdpPortEqAppNamesOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class UdpEqValue1:
    port_numbers: Union[
        OneOfSequencesMatchEntriesPortEqNumbersOptionsDef1,
        OneOfSequencesMatchEntriesPortEqNumbersOptionsDef2,
    ] = _field(metadata={"alias": "portNumbers"})
    app_names: Optional[
        Union[
            OneOfSequencesMatchEntriesUdpPortEqAppNamesOptionsDef1,
            OneOfSequencesMatchEntriesUdpPortEqAppNamesOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "appNames"})


@dataclass
class UdpEqValue2:
    app_names: Union[
        OneOfSequencesMatchEntriesUdpPortEqAppNamesOptionsDef1,
        OneOfSequencesMatchEntriesUdpPortEqAppNamesOptionsDef2,
    ] = _field(metadata={"alias": "appNames"})
    port_numbers: Optional[
        Union[
            OneOfSequencesMatchEntriesPortEqNumbersOptionsDef1,
            OneOfSequencesMatchEntriesPortEqNumbersOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "portNumbers"})


@dataclass
class EqValue2:
    # Match Source UDP Ports That is Equal to Any Value in This List
    udp_eq_value: Union[UdpEqValue1, UdpEqValue2] = _field(metadata={"alias": "udpEqValue"})


@dataclass
class OneOfSequencesMatchEntriesPortRangeStartOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesMatchEntriesPortRangeStartOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSequencesMatchEntriesPortRangeEndOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesMatchEntriesPortRangeEndOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Range:
    """
    Source Port Range
    """

    end: Union[
        OneOfSequencesMatchEntriesPortRangeEndOptionsDef1,
        OneOfSequencesMatchEntriesPortRangeEndOptionsDef2,
    ]
    start: Union[
        OneOfSequencesMatchEntriesPortRangeStartOptionsDef1,
        OneOfSequencesMatchEntriesPortRangeStartOptionsDef2,
    ]


@dataclass
class SourcePorts1:
    operator: Operator
    # Source Port Range
    range: Range
    # Match Source Ports That is Equal to Any Value in This List
    eq_value: Optional[Union[EqValue1, EqValue2]] = _field(
        default=None, metadata={"alias": "eqValue"}
    )
    gt_value: Optional[
        Union[
            OneOfSequencesMatchEntriesPortGtValueOptionsDef1,
            OneOfSequencesMatchEntriesPortGtValueOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "gtValue"})
    lt_value: Optional[
        Union[
            OneOfSequencesMatchEntriesPortLtValueOptionsDef1,
            OneOfSequencesMatchEntriesPortLtValueOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ltValue"})


@dataclass
class OneOfSequencesMatchEntriesPortOperatorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SequencesMatchEntriesPortOperatorDef


@dataclass
class SourcePorts2:
    operator: OneOfSequencesMatchEntriesPortOperatorOptionsDef
    # Match Source Ports That is Equal to Any Value in This List
    eq_value: Optional[Union[EqValue1, EqValue2]] = _field(
        default=None, metadata={"alias": "eqValue"}
    )
    gt_value: Optional[
        Union[
            OneOfSequencesMatchEntriesPortGtValueOptionsDef1,
            OneOfSequencesMatchEntriesPortGtValueOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "gtValue"})
    lt_value: Optional[
        Union[
            OneOfSequencesMatchEntriesPortLtValueOptionsDef1,
            OneOfSequencesMatchEntriesPortLtValueOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ltValue"})
    # Source Port Range
    range: Optional[Range] = _field(default=None)


@dataclass
class OneOfSequencesMatchEntriesDestinationTypeHostOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfSequencesMatchEntriesDestinationHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfSequencesMatchEntriesDestinationHostOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSequencesMatchEntriesDestinationAddressOptionsDef1:
    destination_host: Union[
        OneOfSequencesMatchEntriesDestinationHostOptionsDef1,
        OneOfSequencesMatchEntriesDestinationHostOptionsDef2,
    ] = _field(metadata={"alias": "destinationHost"})
    destination_type: OneOfSequencesMatchEntriesDestinationTypeHostOptionsDef = _field(
        metadata={"alias": "destinationType"}
    )


@dataclass
class OneOfSequencesMatchEntriesDestinationTypeIpPrefixOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfSequencesMatchEntriesDestinationIpPrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSequencesMatchEntriesDestinationIpPrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSequencesMatchEntriesDestinationAddressOptionsDef2:
    destination_ip_prefix: Union[
        OneOfSequencesMatchEntriesDestinationIpPrefixOptionsDef1,
        OneOfSequencesMatchEntriesDestinationIpPrefixOptionsDef2,
    ] = _field(metadata={"alias": "destinationIpPrefix"})
    destination_type: OneOfSequencesMatchEntriesDestinationTypeIpPrefixOptionsDef = _field(
        metadata={"alias": "destinationType"}
    )


@dataclass
class OneOfSequencesMatchEntriesDestinationAddressOptionsDef3:
    destination_network_object_group: ParcelReferenceDef = _field(
        metadata={"alias": "destinationNetworkObjectGroup"}
    )
    destination_type: OneOfSequencesMatchEntriesSourceTypeObjectGroupOptionsDef = _field(
        metadata={"alias": "destinationType"}
    )


@dataclass
class DestinationPorts:
    eq_value: Optional[Any] = _field(default=None, metadata={"alias": "eqValue"})


@dataclass
class OneOfSequencesMatchEntriesIcmpMsgOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfSequencesMatchEntriesIcmpMsgOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSequencesMatchEntriesTcpBitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[SequencesMatchEntriesTcpBitDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSequencesMatchEntriesDscpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfSequencesMatchEntriesDscpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class MatchEntries11:
    protocol: Protocol
    destination_address: Optional[
        Union[
            OneOfSequencesMatchEntriesDestinationAddressOptionsDef1,
            OneOfSequencesMatchEntriesDestinationAddressOptionsDef2,
            OneOfSequencesMatchEntriesDestinationAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "destinationAddress"})
    destination_ports: Optional[DestinationPorts] = _field(
        default=None, metadata={"alias": "destinationPorts"}
    )
    dscp: Optional[
        Union[OneOfSequencesMatchEntriesDscpOptionsDef1, OneOfSequencesMatchEntriesDscpOptionsDef2]
    ] = _field(default=None)
    icmp_msg: Optional[
        Union[
            OneOfSequencesMatchEntriesIcmpMsgOptionsDef1,
            OneOfSequencesMatchEntriesIcmpMsgOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "icmpMsg"})
    source_address: Optional[
        Union[
            OneOfSequencesMatchEntriesSourceAddressOptionsDef1,
            OneOfSequencesMatchEntriesSourceAddressOptionsDef2,
            OneOfSequencesMatchEntriesSourceAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceAddress"})
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )
    tcp_bit: Optional[OneOfSequencesMatchEntriesTcpBitOptionsDef] = _field(
        default=None, metadata={"alias": "tcpBit"}
    )


@dataclass
class OneOfSequencesMatchEntriesProtocolOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class Ipv4AclEqValue1:
    # Match Destination TCP Ports That is Equal to Any Value in This List
    tcp_eq_value: Union[TcpEqValue1, TcpEqValue2] = _field(metadata={"alias": "tcpEqValue"})


@dataclass
class Ipv4AclEqValue2:
    # Match Destination UDP Ports That is Equal to Any Value in This List
    udp_eq_value: Union[UdpEqValue1, UdpEqValue2] = _field(metadata={"alias": "udpEqValue"})


@dataclass
class Ipv4AclRange:
    """
    Destination Port Range
    """

    end: Optional[
        Union[
            OneOfSequencesMatchEntriesPortRangeEndOptionsDef1,
            OneOfSequencesMatchEntriesPortRangeEndOptionsDef2,
        ]
    ] = _field(default=None)
    start: Optional[
        Union[
            OneOfSequencesMatchEntriesPortRangeStartOptionsDef1,
            OneOfSequencesMatchEntriesPortRangeStartOptionsDef2,
        ]
    ] = _field(default=None)


@dataclass
class DestinationPorts1:
    operator: Operator
    # Destination Port Range
    range: Ipv4AclRange
    # Match Destination Ports That is Equal to Any Value in This List
    eq_value: Optional[Union[Ipv4AclEqValue1, Ipv4AclEqValue2]] = _field(
        default=None, metadata={"alias": "eqValue"}
    )
    gt_value: Optional[
        Union[
            OneOfSequencesMatchEntriesPortGtValueOptionsDef1,
            OneOfSequencesMatchEntriesPortGtValueOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "gtValue"})
    lt_value: Optional[
        Union[
            OneOfSequencesMatchEntriesPortLtValueOptionsDef1,
            OneOfSequencesMatchEntriesPortLtValueOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ltValue"})


@dataclass
class ServiceIpv4AclEqValue1:
    # Match Destination TCP Ports That is Equal to Any Value in This List
    tcp_eq_value: Union[TcpEqValue1, TcpEqValue2] = _field(metadata={"alias": "tcpEqValue"})


@dataclass
class ServiceIpv4AclEqValue2:
    # Match Destination UDP Ports That is Equal to Any Value in This List
    udp_eq_value: Union[UdpEqValue1, UdpEqValue2] = _field(metadata={"alias": "udpEqValue"})


@dataclass
class ServiceIpv4AclRange:
    """
    Destination Port Range
    """

    end: Optional[
        Union[
            OneOfSequencesMatchEntriesPortRangeEndOptionsDef1,
            OneOfSequencesMatchEntriesPortRangeEndOptionsDef2,
        ]
    ] = _field(default=None)
    start: Optional[
        Union[
            OneOfSequencesMatchEntriesPortRangeStartOptionsDef1,
            OneOfSequencesMatchEntriesPortRangeStartOptionsDef2,
        ]
    ] = _field(default=None)


@dataclass
class DestinationPorts2:
    operator: OneOfSequencesMatchEntriesPortOperatorOptionsDef
    # Match Destination Ports That is Equal to Any Value in This List
    eq_value: Optional[Union[ServiceIpv4AclEqValue1, ServiceIpv4AclEqValue2]] = _field(
        default=None, metadata={"alias": "eqValue"}
    )
    gt_value: Optional[
        Union[
            OneOfSequencesMatchEntriesPortGtValueOptionsDef1,
            OneOfSequencesMatchEntriesPortGtValueOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "gtValue"})
    lt_value: Optional[
        Union[
            OneOfSequencesMatchEntriesPortLtValueOptionsDef1,
            OneOfSequencesMatchEntriesPortLtValueOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ltValue"})
    # Destination Port Range
    range: Optional[ServiceIpv4AclRange] = _field(default=None)


@dataclass
class MatchEntries12:
    protocol: OneOfSequencesMatchEntriesProtocolOptionsDef
    destination_address: Optional[
        Union[
            OneOfSequencesMatchEntriesDestinationAddressOptionsDef1,
            OneOfSequencesMatchEntriesDestinationAddressOptionsDef2,
            OneOfSequencesMatchEntriesDestinationAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "destinationAddress"})
    # Destination Ports
    destination_ports: Optional[Union[DestinationPorts1, DestinationPorts2]] = _field(
        default=None, metadata={"alias": "destinationPorts"}
    )
    dscp: Optional[
        Union[OneOfSequencesMatchEntriesDscpOptionsDef1, OneOfSequencesMatchEntriesDscpOptionsDef2]
    ] = _field(default=None)
    icmp_msg: Optional[
        Union[
            OneOfSequencesMatchEntriesIcmpMsgOptionsDef1,
            OneOfSequencesMatchEntriesIcmpMsgOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "icmpMsg"})
    source_address: Optional[
        Union[
            OneOfSequencesMatchEntriesSourceAddressOptionsDef1,
            OneOfSequencesMatchEntriesSourceAddressOptionsDef2,
            OneOfSequencesMatchEntriesSourceAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceAddress"})
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )
    tcp_bit: Optional[OneOfSequencesMatchEntriesTcpBitOptionsDef] = _field(
        default=None, metadata={"alias": "tcpBit"}
    )


@dataclass
class MatchEntries2:
    service_object_group: ParcelReferenceDef = _field(metadata={"alias": "serviceObjectGroup"})
    destination_address: Optional[
        Union[
            OneOfSequencesMatchEntriesDestinationAddressOptionsDef1,
            OneOfSequencesMatchEntriesDestinationAddressOptionsDef2,
            OneOfSequencesMatchEntriesDestinationAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "destinationAddress"})
    dscp: Optional[
        Union[OneOfSequencesMatchEntriesDscpOptionsDef1, OneOfSequencesMatchEntriesDscpOptionsDef2]
    ] = _field(default=None)
    source_address: Optional[
        Union[
            OneOfSequencesMatchEntriesSourceAddressOptionsDef1,
            OneOfSequencesMatchEntriesSourceAddressOptionsDef2,
            OneOfSequencesMatchEntriesSourceAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceAddress"})


@dataclass
class ExtendedAclSequences2:
    action_type: Union[OneOfSequencesActionTypeOptionsDef1, OneOfSequencesActionTypeOptionsDef2] = (
        _field(metadata={"alias": "actionType"})
    )
    # Define match conditions
    match_entries: Union[Union[MatchEntries11, MatchEntries12], MatchEntries2] = _field(
        metadata={"alias": "matchEntries"}
    )
    sequence_name: OneOfSequencesSequenceNameOptionsDef = _field(metadata={"alias": "sequenceName"})
    # Actions
    actions: Optional[Union[Actions1, Actions2]] = _field(default=None)


@dataclass
class Ipv4AclData:
    acl_type: OneOfAclTypeOptionsDef = _field(metadata={"alias": "aclType"})
    default_action: Union[OneOfDefaultActionOptionsDef1, OneOfDefaultActionOptionsDef2] = _field(
        metadata={"alias": "defaultAction"}
    )
    # Sequences for extended ACL
    extended_acl_sequences: Optional[List[Union[ExtendedAclSequences1, ExtendedAclSequences2]]] = (
        _field(default=None, metadata={"alias": "extendedAclSequences"})
    )
    # Sequences for extended ACL
    standard_acl_sequences: Optional[List[StandardAclSequences]] = _field(
        default=None, metadata={"alias": "standardAclSequences"}
    )


@dataclass
class Payload:
    """
    SD-Routing IPv4 ACL feature schema
    """

    data: Ipv4AclData
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
    # SD-Routing IPv4 ACL feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingServiceIpv4AclPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingServiceIpv4AclFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceIpv4AclData:
    acl_type: OneOfAclTypeOptionsDef = _field(metadata={"alias": "aclType"})
    default_action: Union[OneOfDefaultActionOptionsDef1, OneOfDefaultActionOptionsDef2] = _field(
        metadata={"alias": "defaultAction"}
    )
    # Sequences for extended ACL
    extended_acl_sequences: Optional[List[Union[ExtendedAclSequences1, ExtendedAclSequences2]]] = (
        _field(default=None, metadata={"alias": "extendedAclSequences"})
    )
    # Sequences for extended ACL
    standard_acl_sequences: Optional[List[StandardAclSequences]] = _field(
        default=None, metadata={"alias": "standardAclSequences"}
    )


@dataclass
class CreateSdroutingServiceIpv4AclFeaturePostRequest:
    """
    SD-Routing IPv4 ACL feature schema
    """

    data: ServiceIpv4AclData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingServiceIpv4AclPayload:
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
    # SD-Routing IPv4 ACL feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingServiceIpv4AclFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingServiceIpv4AclData:
    acl_type: OneOfAclTypeOptionsDef = _field(metadata={"alias": "aclType"})
    default_action: Union[OneOfDefaultActionOptionsDef1, OneOfDefaultActionOptionsDef2] = _field(
        metadata={"alias": "defaultAction"}
    )
    # Sequences for extended ACL
    extended_acl_sequences: Optional[List[Union[ExtendedAclSequences1, ExtendedAclSequences2]]] = (
        _field(default=None, metadata={"alias": "extendedAclSequences"})
    )
    # Sequences for extended ACL
    standard_acl_sequences: Optional[List[StandardAclSequences]] = _field(
        default=None, metadata={"alias": "standardAclSequences"}
    )


@dataclass
class EditSdroutingServiceIpv4AclFeaturePutRequest:
    """
    SD-Routing IPv4 ACL feature schema
    """

    data: SdRoutingServiceIpv4AclData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
