# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

RefTypeDef = Literal["esimcellular-profile"]

EsimcellularControllerRefTypeDef = Literal["esimcellular-profile"]

TransportEsimcellularControllerRefTypeDef = Literal["esimcellular-profile"]

SdwanTransportEsimcellularControllerRefTypeDef = Literal["esimcellular-profile"]

FeatureProfileSdwanTransportEsimcellularControllerRefTypeDef = Literal["esimcellular-profile"]


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
class OneOfEsimSlotOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


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
class EsimControllerConfigDef:
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
    slot: Optional[OneOfEsimSlotOptionsDef] = _field(default=None)


@dataclass
class RefIdOptionDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RefTypeOptionDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RefTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ProfileRefOptionDef:
    ref_id: RefIdOptionDef = _field(metadata={"alias": "refId"})
    ref_type: RefTypeOptionDef = _field(metadata={"alias": "refType"})


@dataclass
class CommonSlotConfigDef:
    """
    Set the slot specific attach and data profile feature ids
    """

    attach_profile: ProfileRefOptionDef = _field(metadata={"alias": "attachProfile"})
    data_profile: Optional[ProfileRefOptionDef] = _field(
        default=None, metadata={"alias": "dataProfile"}
    )


@dataclass
class SlotConfigDef:
    """
    Set the slot specific attach and data profile feature ids
    """

    # Set the slot specific attach and data profile feature ids
    slot0_config: CommonSlotConfigDef = _field(metadata={"alias": "slot0Config"})


@dataclass
class EsimControllerConfigOptionDef:
    """
    eSim Cellular controller config
    """

    controller_config: EsimControllerConfigDef = _field(metadata={"alias": "controllerConfig"})
    # Set the slot specific attach and data profile feature ids
    slot_config: SlotConfigDef = _field(metadata={"alias": "slotConfig"})


@dataclass
class Payload:
    """
    eSimCellularController feature schema for POST request
    """

    # eSim Cellular controller config
    data: EsimControllerConfigOptionDef
    name: str
    # Set the eSimCellularController feature schema description
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
    # eSimCellularController feature schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportEsimcellularControllerPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateEsimCellularControllerProfileFeatureForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateEsimCellularControllerProfileFeatureForTransportPostRequest:
    """
    eSimCellularController feature schema for POST request
    """

    # eSim Cellular controller config
    data: EsimControllerConfigOptionDef
    name: str
    # Set the eSimCellularController feature schema description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EsimcellularControllerOneOfIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EsimcellularControllerOneOfMaxRetryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EsimcellularControllerOneOfFailovertimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EsimcellularControllerEsimControllerConfigDef:
    id: Union[EsimcellularControllerOneOfIdOptionsDef1, OneOfIdOptionsDef2]
    auto_sim: Optional[
        Union[OneOfAutoSimOptionsDef1, OneOfAutoSimOptionsDef2, OneOfAutoSimOptionsDef3]
    ] = _field(default=None, metadata={"alias": "autoSim"})
    failovertimer: Optional[
        Union[
            EsimcellularControllerOneOfFailovertimerOptionsDef1,
            OneOfFailovertimerOptionsDef2,
            OneOfFailovertimerOptionsDef3,
        ]
    ] = _field(default=None)
    max_retry: Optional[
        Union[
            EsimcellularControllerOneOfMaxRetryOptionsDef1,
            OneOfMaxRetryOptionsDef2,
            OneOfMaxRetryOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxRetry"})
    slot: Optional[OneOfEsimSlotOptionsDef] = _field(default=None)


@dataclass
class EsimcellularControllerRefTypeOptionDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EsimcellularControllerRefTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EsimcellularControllerProfileRefOptionDef:
    ref_id: RefIdOptionDef = _field(metadata={"alias": "refId"})
    ref_type: EsimcellularControllerRefTypeOptionDef = _field(metadata={"alias": "refType"})


@dataclass
class TransportEsimcellularControllerRefTypeOptionDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportEsimcellularControllerRefTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class TransportEsimcellularControllerProfileRefOptionDef:
    ref_id: RefIdOptionDef = _field(metadata={"alias": "refId"})
    ref_type: TransportEsimcellularControllerRefTypeOptionDef = _field(
        metadata={"alias": "refType"}
    )


@dataclass
class EsimcellularControllerCommonSlotConfigDef:
    """
    Set the slot specific attach and data profile feature ids
    """

    attach_profile: EsimcellularControllerProfileRefOptionDef = _field(
        metadata={"alias": "attachProfile"}
    )
    data_profile: Optional[TransportEsimcellularControllerProfileRefOptionDef] = _field(
        default=None, metadata={"alias": "dataProfile"}
    )


@dataclass
class EsimcellularControllerSlotConfigDef:
    """
    Set the slot specific attach and data profile feature ids
    """

    # Set the slot specific attach and data profile feature ids
    slot0_config: EsimcellularControllerCommonSlotConfigDef = _field(
        metadata={"alias": "slot0Config"}
    )


@dataclass
class EsimcellularControllerEsimControllerConfigOptionDef:
    """
    eSim Cellular controller config
    """

    controller_config: EsimcellularControllerEsimControllerConfigDef = _field(
        metadata={"alias": "controllerConfig"}
    )
    # Set the slot specific attach and data profile feature ids
    slot_config: EsimcellularControllerSlotConfigDef = _field(metadata={"alias": "slotConfig"})


@dataclass
class EsimcellularControllerPayload:
    """
    eSimCellularController feature schema for PUT request
    """

    # eSim Cellular controller config
    data: EsimcellularControllerEsimControllerConfigOptionDef
    name: str
    # Set the eSimCellularController feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanTransportEsimcellularControllerPayload:
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
    # eSimCellularController feature schema for PUT request
    payload: Optional[EsimcellularControllerPayload] = _field(default=None)


@dataclass
class EditEsimCellularControllerProfileFeatureForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportEsimcellularControllerOneOfIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportEsimcellularControllerOneOfMaxRetryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportEsimcellularControllerOneOfFailovertimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportEsimcellularControllerEsimControllerConfigDef:
    id: Union[TransportEsimcellularControllerOneOfIdOptionsDef1, OneOfIdOptionsDef2]
    auto_sim: Optional[
        Union[OneOfAutoSimOptionsDef1, OneOfAutoSimOptionsDef2, OneOfAutoSimOptionsDef3]
    ] = _field(default=None, metadata={"alias": "autoSim"})
    failovertimer: Optional[
        Union[
            TransportEsimcellularControllerOneOfFailovertimerOptionsDef1,
            OneOfFailovertimerOptionsDef2,
            OneOfFailovertimerOptionsDef3,
        ]
    ] = _field(default=None)
    max_retry: Optional[
        Union[
            TransportEsimcellularControllerOneOfMaxRetryOptionsDef1,
            OneOfMaxRetryOptionsDef2,
            OneOfMaxRetryOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxRetry"})
    slot: Optional[OneOfEsimSlotOptionsDef] = _field(default=None)


@dataclass
class SdwanTransportEsimcellularControllerRefTypeOptionDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        SdwanTransportEsimcellularControllerRefTypeDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class SdwanTransportEsimcellularControllerProfileRefOptionDef:
    ref_id: RefIdOptionDef = _field(metadata={"alias": "refId"})
    ref_type: SdwanTransportEsimcellularControllerRefTypeOptionDef = _field(
        metadata={"alias": "refType"}
    )


@dataclass
class FeatureProfileSdwanTransportEsimcellularControllerRefTypeOptionDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanTransportEsimcellularControllerRefTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdwanTransportEsimcellularControllerProfileRefOptionDef:
    ref_id: RefIdOptionDef = _field(metadata={"alias": "refId"})
    ref_type: FeatureProfileSdwanTransportEsimcellularControllerRefTypeOptionDef = _field(
        metadata={"alias": "refType"}
    )


@dataclass
class TransportEsimcellularControllerCommonSlotConfigDef:
    """
    Set the slot specific attach and data profile feature ids
    """

    attach_profile: SdwanTransportEsimcellularControllerProfileRefOptionDef = _field(
        metadata={"alias": "attachProfile"}
    )
    data_profile: Optional[
        FeatureProfileSdwanTransportEsimcellularControllerProfileRefOptionDef
    ] = _field(default=None, metadata={"alias": "dataProfile"})


@dataclass
class TransportEsimcellularControllerSlotConfigDef:
    """
    Set the slot specific attach and data profile feature ids
    """

    # Set the slot specific attach and data profile feature ids
    slot0_config: TransportEsimcellularControllerCommonSlotConfigDef = _field(
        metadata={"alias": "slot0Config"}
    )


@dataclass
class TransportEsimcellularControllerEsimControllerConfigOptionDef:
    """
    eSim Cellular controller config
    """

    controller_config: TransportEsimcellularControllerEsimControllerConfigDef = _field(
        metadata={"alias": "controllerConfig"}
    )
    # Set the slot specific attach and data profile feature ids
    slot_config: TransportEsimcellularControllerSlotConfigDef = _field(
        metadata={"alias": "slotConfig"}
    )


@dataclass
class EditEsimCellularControllerProfileFeatureForTransportPutRequest:
    """
    eSimCellularController feature schema for PUT request
    """

    # eSim Cellular controller config
    data: TransportEsimcellularControllerEsimControllerConfigOptionDef
    name: str
    # Set the eSimCellularController feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
