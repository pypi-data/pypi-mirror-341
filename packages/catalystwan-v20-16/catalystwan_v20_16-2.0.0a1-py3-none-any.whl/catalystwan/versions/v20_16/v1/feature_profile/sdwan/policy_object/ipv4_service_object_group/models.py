# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class OneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDescriptionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDescriptionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class Entries1:
    object_group: ParcelReferenceDef = _field(metadata={"alias": "objectGroup"})


@dataclass
class Protocol:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesOperatorLtOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesPortLtValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesPortLtValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SourcePorts1:
    lt_value: Union[OneOfEntriesPortLtValueOptionsDef1, OneOfEntriesPortLtValueOptionsDef2] = (
        _field(metadata={"alias": "ltValue"})
    )
    operator: OneOfEntriesOperatorLtOptionsDef


@dataclass
class OneOfEntriesOperatorEqOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesTcpPortEqValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfEntriesTcpPortEqValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class EqValue1:
    tcp_eq_value: Union[
        OneOfEntriesTcpPortEqValueOptionsDef1, OneOfEntriesTcpPortEqValueOptionsDef2
    ] = _field(metadata={"alias": "tcpEqValue"})


@dataclass
class OneOfEntriesUdpPortEqValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfEntriesUdpPortEqValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class EqValue2:
    udp_eq_value: Union[
        OneOfEntriesUdpPortEqValueOptionsDef1, OneOfEntriesUdpPortEqValueOptionsDef2
    ] = _field(metadata={"alias": "udpEqValue"})


@dataclass
class OneOfEntriesTcpUdpPortEqValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfEntriesTcpUdpPortEqValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class EqValue3:
    tcp_udp_eq_value: Union[
        OneOfEntriesTcpUdpPortEqValueOptionsDef1, OneOfEntriesTcpUdpPortEqValueOptionsDef2
    ] = _field(metadata={"alias": "tcpUdpEqValue"})


@dataclass
class SourcePorts2:
    # Source Port That is Equal to This Value
    eq_value: Union[EqValue1, EqValue2, EqValue3] = _field(metadata={"alias": "eqValue"})
    operator: OneOfEntriesOperatorEqOptionsDef


@dataclass
class OneOfEntriesOperatorGtOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesPortGtValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesPortGtValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SourcePorts3:
    gt_value: Union[OneOfEntriesPortGtValueOptionsDef1, OneOfEntriesPortGtValueOptionsDef2] = (
        _field(metadata={"alias": "gtValue"})
    )
    operator: OneOfEntriesOperatorGtOptionsDef


@dataclass
class OneOfEntriesOperatorRangeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesPortRangeStartOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesPortRangeStartOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEntriesPortRangeEndOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesPortRangeEndOptionsDef2:
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

    end: Union[OneOfEntriesPortRangeEndOptionsDef1, OneOfEntriesPortRangeEndOptionsDef2]
    start: Union[OneOfEntriesPortRangeStartOptionsDef1, OneOfEntriesPortRangeStartOptionsDef2]


@dataclass
class SourcePorts4:
    operator: OneOfEntriesOperatorRangeOptionsDef
    # Source Port Range
    range: Range


@dataclass
class DestinationPorts:
    eq_value: Optional[Any] = _field(default=None, metadata={"alias": "eqValue"})


@dataclass
class OneOfEntriesIcmpMsgOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfEntriesIcmpMsgOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Entries21:
    protocol: Protocol
    destination_ports: Optional[DestinationPorts] = _field(
        default=None, metadata={"alias": "destinationPorts"}
    )
    icmp_msg: Optional[Union[OneOfEntriesIcmpMsgOptionsDef1, OneOfEntriesIcmpMsgOptionsDef2]] = (
        _field(default=None, metadata={"alias": "icmpMsg"})
    )
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2, SourcePorts3, SourcePorts4]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )


@dataclass
class OneOfEntriesProtocolOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class DestinationPorts1:
    lt_value: Union[OneOfEntriesPortLtValueOptionsDef1, OneOfEntriesPortLtValueOptionsDef2] = (
        _field(metadata={"alias": "ltValue"})
    )
    operator: OneOfEntriesOperatorLtOptionsDef


@dataclass
class DestinationPorts2:
    # Destination Port That is Equal to This Value
    eq_value: Union[EqValue1, EqValue2, EqValue3] = _field(metadata={"alias": "eqValue"})
    operator: OneOfEntriesOperatorEqOptionsDef


@dataclass
class DestinationPorts3:
    gt_value: Union[OneOfEntriesPortGtValueOptionsDef1, OneOfEntriesPortGtValueOptionsDef2] = (
        _field(metadata={"alias": "gtValue"})
    )
    operator: OneOfEntriesOperatorGtOptionsDef


@dataclass
class Ipv4ServiceObjectGroupRange:
    """
    Destination Port Range
    """

    end: Union[OneOfEntriesPortRangeEndOptionsDef1, OneOfEntriesPortRangeEndOptionsDef2]
    start: Union[OneOfEntriesPortRangeStartOptionsDef1, OneOfEntriesPortRangeStartOptionsDef2]


@dataclass
class DestinationPorts4:
    operator: OneOfEntriesOperatorRangeOptionsDef
    # Destination Port Range
    range: Ipv4ServiceObjectGroupRange


@dataclass
class Entries22:
    protocol: OneOfEntriesProtocolOptionsDef
    # Destination Ports
    destination_ports: Optional[
        Union[DestinationPorts1, DestinationPorts2, DestinationPorts3, DestinationPorts4]
    ] = _field(default=None, metadata={"alias": "destinationPorts"})
    icmp_msg: Optional[Union[OneOfEntriesIcmpMsgOptionsDef1, OneOfEntriesIcmpMsgOptionsDef2]] = (
        _field(default=None, metadata={"alias": "icmpMsg"})
    )
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2, SourcePorts3, SourcePorts4]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )


@dataclass
class Data:
    # object-group Entries
    entries: List[Union[Entries1, Union[Entries21, Entries22]]]
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest:
    """
    Ipv4 Service Object Group profile parcel schema
    """

    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload:
    """
    Ipv4 Service Object Group profile parcel schema
    """

    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetDataPrefixProfileParcelForPolicyObjectGetResponse:
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # Ipv4 Service Object Group profile parcel schema
    payload: Optional[Payload] = _field(default=None)
