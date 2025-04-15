# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

DefaultOptionTypeDef = Literal["default"]

Value = Literal["non-eSim"]

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]


@dataclass
class ConfigType:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSlotOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSlotOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSlotOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMaxRetryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMaxRetryOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMaxRetryOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfFailovertimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfFailovertimerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfFailovertimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAutoSimOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAutoSimOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAutoSimOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class CommonControllerConfigDef:
    id: Union[OneOfIdOptionsDef1, OneOfIdOptionsDef2]
    auto_sim: Optional[
        Union[OneOfAutoSimOptionsDef1, OneOfAutoSimOptionsDef2, OneOfAutoSimOptionsDef3]
    ] = _field(default=None, metadata={"alias": "autoSim"})
    failovertimer: Optional[
        Union[
            OneOfFailovertimerOptionsDef1,
            OneOfFailovertimerOptionsDef2,
            OneOfFailovertimerOptionsDef3,
        ]
    ] = _field(default=None)
    max_retry: Optional[
        Union[OneOfMaxRetryOptionsDef1, OneOfMaxRetryOptionsDef2, OneOfMaxRetryOptionsDef3]
    ] = _field(default=None, metadata={"alias": "maxRetry"})
    slot: Optional[Union[OneOfSlotOptionsDef1, OneOfSlotOptionsDef2, OneOfSlotOptionsDef3]] = (
        _field(default=None)
    )


@dataclass
class NonEsimControllerConfigDef:
    """
    Regular Cellular controller (non-eSim) config
    """

    config_type: ConfigType = _field(metadata={"alias": "configType"})
    controller_config: CommonControllerConfigDef = _field(metadata={"alias": "controllerConfig"})


@dataclass
class Payload:
    """
    CellularController profile parcel schema for POST request
    """

    data: NonEsimControllerConfigDef
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
    # CellularController profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingTransportCellularControllerPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateCellularControllerProfileParcelForTransport1PostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateCellularControllerProfileParcelForTransport1PostRequest:
    """
    CellularController profile parcel schema for POST request
    """

    data: NonEsimControllerConfigDef
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CellularControllerOneOfIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularControllerOneOfSlotOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularControllerOneOfMaxRetryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularControllerOneOfFailovertimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularControllerCommonControllerConfigDef:
    id: Union[CellularControllerOneOfIdOptionsDef1, OneOfIdOptionsDef2]
    auto_sim: Optional[
        Union[OneOfAutoSimOptionsDef1, OneOfAutoSimOptionsDef2, OneOfAutoSimOptionsDef3]
    ] = _field(default=None, metadata={"alias": "autoSim"})
    failovertimer: Optional[
        Union[
            CellularControllerOneOfFailovertimerOptionsDef1,
            OneOfFailovertimerOptionsDef2,
            OneOfFailovertimerOptionsDef3,
        ]
    ] = _field(default=None)
    max_retry: Optional[
        Union[
            CellularControllerOneOfMaxRetryOptionsDef1,
            OneOfMaxRetryOptionsDef2,
            OneOfMaxRetryOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxRetry"})
    slot: Optional[
        Union[CellularControllerOneOfSlotOptionsDef1, OneOfSlotOptionsDef2, OneOfSlotOptionsDef3]
    ] = _field(default=None)


@dataclass
class CellularControllerNonEsimControllerConfigDef:
    """
    Regular Cellular controller (non-eSim) config
    """

    config_type: ConfigType = _field(metadata={"alias": "configType"})
    controller_config: CellularControllerCommonControllerConfigDef = _field(
        metadata={"alias": "controllerConfig"}
    )


@dataclass
class CellularControllerPayload:
    """
    CellularController profile parcel schema for PUT request
    """

    data: CellularControllerNonEsimControllerConfigDef
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingTransportCellularControllerPayload:
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
    # CellularController profile parcel schema for PUT request
    payload: Optional[CellularControllerPayload] = _field(default=None)


@dataclass
class EditCellularControllerProfileParcelForTransport1PutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportCellularControllerOneOfIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportCellularControllerOneOfSlotOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportCellularControllerOneOfMaxRetryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportCellularControllerOneOfFailovertimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportCellularControllerCommonControllerConfigDef:
    id: Union[TransportCellularControllerOneOfIdOptionsDef1, OneOfIdOptionsDef2]
    auto_sim: Optional[
        Union[OneOfAutoSimOptionsDef1, OneOfAutoSimOptionsDef2, OneOfAutoSimOptionsDef3]
    ] = _field(default=None, metadata={"alias": "autoSim"})
    failovertimer: Optional[
        Union[
            TransportCellularControllerOneOfFailovertimerOptionsDef1,
            OneOfFailovertimerOptionsDef2,
            OneOfFailovertimerOptionsDef3,
        ]
    ] = _field(default=None)
    max_retry: Optional[
        Union[
            TransportCellularControllerOneOfMaxRetryOptionsDef1,
            OneOfMaxRetryOptionsDef2,
            OneOfMaxRetryOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxRetry"})
    slot: Optional[
        Union[
            TransportCellularControllerOneOfSlotOptionsDef1,
            OneOfSlotOptionsDef2,
            OneOfSlotOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class TransportCellularControllerNonEsimControllerConfigDef:
    """
    Regular Cellular controller (non-eSim) config
    """

    config_type: ConfigType = _field(metadata={"alias": "configType"})
    controller_config: TransportCellularControllerCommonControllerConfigDef = _field(
        metadata={"alias": "controllerConfig"}
    )


@dataclass
class EditCellularControllerProfileParcelForTransport1PutRequest:
    """
    CellularController profile parcel schema for PUT request
    """

    data: TransportCellularControllerNonEsimControllerConfigDef
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
