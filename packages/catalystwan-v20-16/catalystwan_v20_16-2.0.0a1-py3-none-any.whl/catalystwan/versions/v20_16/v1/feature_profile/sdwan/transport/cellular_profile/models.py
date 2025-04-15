# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

DefaultOptionTypeDef = Literal["default"]

Value = Literal["non-eSim"]

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultAuthenticationDef = Literal["none"]

AuthenticationDef = Literal["chap", "pap", "pap_chap"]

PdnTypeDef = Literal["ipv4", "ipv4v6", "ipv6"]

DefaultPdnTypeDef = Literal["ipv4"]

CellularProfileDefaultAuthenticationDef = Literal["none"]

CellularProfileAuthenticationDef = Literal["chap", "pap", "pap_chap"]

CellularProfilePdnTypeDef = Literal["ipv4", "ipv4v6", "ipv6"]

CellularProfileDefaultPdnTypeDef = Literal["ipv4"]

TransportCellularProfileDefaultAuthenticationDef = Literal["none"]

TransportCellularProfileAuthenticationDef = Literal["chap", "pap", "pap_chap"]

TransportCellularProfilePdnTypeDef = Literal["ipv4", "ipv4v6", "ipv6"]

TransportCellularProfileDefaultPdnTypeDef = Literal["ipv4"]


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
    value: int


@dataclass
class OneOfIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfApnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfApnOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDefaultAuthenticationOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Authentication1:
    no_authentication: OneOfDefaultAuthenticationOptionsDef = _field(
        metadata={"alias": "noAuthentication"}
    )


@dataclass
class OneOfAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAuthenticationOptionsDef2:
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
    value: str


@dataclass
class OneOfPasswordOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class NeedAuthentication:
    password: Union[OneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    type_: Union[OneOfAuthenticationOptionsDef1, OneOfAuthenticationOptionsDef2] = _field(
        metadata={"alias": "type"}
    )
    username: Union[OneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class Authentication2:
    need_authentication: NeedAuthentication = _field(metadata={"alias": "needAuthentication"})


@dataclass
class OneOfPdnTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PdnTypeDef


@dataclass
class OneOfPdnTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPdnTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultPdnTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNoOverwriteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNoOverwriteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNoOverwriteOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSliceTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSliceTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSliceTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSliceDifferentiatorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSliceDifferentiatorOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSliceDifferentiatorOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class NetworkSlicing:
    slice_differentiator: Optional[
        Union[
            OneOfSliceDifferentiatorOptionsDef1,
            OneOfSliceDifferentiatorOptionsDef2,
            OneOfSliceDifferentiatorOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sliceDifferentiator"})
    slice_type: Optional[
        Union[OneOfSliceTypeOptionsDef1, OneOfSliceTypeOptionsDef2, OneOfSliceTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "sliceType"})


@dataclass
class CommonCellularProfileInfoDef:
    apn: Union[OneOfApnOptionsDef1, OneOfApnOptionsDef2]
    authentication: Optional[Union[Authentication1, Authentication2]] = _field(default=None)
    network_slicing: Optional[NetworkSlicing] = _field(
        default=None, metadata={"alias": "networkSlicing"}
    )
    no_overwrite: Optional[
        Union[OneOfNoOverwriteOptionsDef1, OneOfNoOverwriteOptionsDef2, OneOfNoOverwriteOptionsDef3]
    ] = _field(default=None, metadata={"alias": "noOverwrite"})
    pdn_type: Optional[
        Union[OneOfPdnTypeOptionsDef1, OneOfPdnTypeOptionsDef2, OneOfPdnTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class ProfileConfig:
    id: Union[OneOfIdOptionsDef1, OneOfIdOptionsDef2]
    profile_info: CommonCellularProfileInfoDef = _field(metadata={"alias": "profileInfo"})


@dataclass
class NonEsimCellularProfileConfigDef:
    """
    Regular Cellular profile (non-eSim) config
    """

    config_type: ConfigType = _field(metadata={"alias": "configType"})
    profile_config: ProfileConfig = _field(metadata={"alias": "profileConfig"})


@dataclass
class Payload:
    """
    CellularProfile profile parcel schema for POST request
    """

    data: NonEsimCellularProfileConfigDef
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
    # CellularProfile profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportCellularProfilePayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateCellularProfileProfileParcelForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateCellularProfileProfileParcelForTransportPostRequest:
    """
    CellularProfile profile parcel schema for POST request
    """

    data: NonEsimCellularProfileConfigDef
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CellularProfileOneOfIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularProfileOneOfApnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularProfileOneOfDefaultAuthenticationOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularProfileDefaultAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularProfileAuthentication1:
    no_authentication: CellularProfileOneOfDefaultAuthenticationOptionsDef = _field(
        metadata={"alias": "noAuthentication"}
    )


@dataclass
class CellularProfileOneOfAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularProfileAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularProfileOneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularProfileOneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularProfileNeedAuthentication:
    password: Union[CellularProfileOneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    type_: Union[CellularProfileOneOfAuthenticationOptionsDef1, OneOfAuthenticationOptionsDef2] = (
        _field(metadata={"alias": "type"})
    )
    username: Union[CellularProfileOneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class CellularProfileAuthentication2:
    need_authentication: CellularProfileNeedAuthentication = _field(
        metadata={"alias": "needAuthentication"}
    )


@dataclass
class CellularProfileOneOfPdnTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularProfilePdnTypeDef


@dataclass
class CellularProfileOneOfPdnTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularProfileDefaultPdnTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularProfileOneOfSliceTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularProfileOneOfSliceDifferentiatorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularProfileNetworkSlicing:
    slice_differentiator: Optional[
        Union[
            CellularProfileOneOfSliceDifferentiatorOptionsDef1,
            OneOfSliceDifferentiatorOptionsDef2,
            OneOfSliceDifferentiatorOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sliceDifferentiator"})
    slice_type: Optional[
        Union[
            CellularProfileOneOfSliceTypeOptionsDef1,
            OneOfSliceTypeOptionsDef2,
            OneOfSliceTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sliceType"})


@dataclass
class CellularProfileCommonCellularProfileInfoDef:
    apn: Union[CellularProfileOneOfApnOptionsDef1, OneOfApnOptionsDef2]
    authentication: Optional[
        Union[CellularProfileAuthentication1, CellularProfileAuthentication2]
    ] = _field(default=None)
    network_slicing: Optional[CellularProfileNetworkSlicing] = _field(
        default=None, metadata={"alias": "networkSlicing"}
    )
    no_overwrite: Optional[
        Union[OneOfNoOverwriteOptionsDef1, OneOfNoOverwriteOptionsDef2, OneOfNoOverwriteOptionsDef3]
    ] = _field(default=None, metadata={"alias": "noOverwrite"})
    pdn_type: Optional[
        Union[
            CellularProfileOneOfPdnTypeOptionsDef1,
            OneOfPdnTypeOptionsDef2,
            CellularProfileOneOfPdnTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class CellularProfileProfileConfig:
    id: Union[CellularProfileOneOfIdOptionsDef1, OneOfIdOptionsDef2]
    profile_info: CellularProfileCommonCellularProfileInfoDef = _field(
        metadata={"alias": "profileInfo"}
    )


@dataclass
class CellularProfileNonEsimCellularProfileConfigDef:
    """
    Regular Cellular profile (non-eSim) config
    """

    config_type: ConfigType = _field(metadata={"alias": "configType"})
    profile_config: CellularProfileProfileConfig = _field(metadata={"alias": "profileConfig"})


@dataclass
class CellularProfilePayload:
    """
    CellularProfile profile parcel schema for PUT request
    """

    data: CellularProfileNonEsimCellularProfileConfigDef
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanTransportCellularProfilePayload:
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
    # CellularProfile profile parcel schema for PUT request
    payload: Optional[CellularProfilePayload] = _field(default=None)


@dataclass
class EditCellularProfileProfileParcelForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportCellularProfileOneOfIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportCellularProfileOneOfApnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportCellularProfileOneOfDefaultAuthenticationOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        TransportCellularProfileDefaultAuthenticationDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class TransportCellularProfileAuthentication1:
    no_authentication: TransportCellularProfileOneOfDefaultAuthenticationOptionsDef = _field(
        metadata={"alias": "noAuthentication"}
    )


@dataclass
class TransportCellularProfileOneOfAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportCellularProfileAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class TransportCellularProfileOneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportCellularProfileOneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportCellularProfileNeedAuthentication:
    password: Union[TransportCellularProfileOneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    type_: Union[
        TransportCellularProfileOneOfAuthenticationOptionsDef1, OneOfAuthenticationOptionsDef2
    ] = _field(metadata={"alias": "type"})
    username: Union[TransportCellularProfileOneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class TransportCellularProfileAuthentication2:
    need_authentication: TransportCellularProfileNeedAuthentication = _field(
        metadata={"alias": "needAuthentication"}
    )


@dataclass
class TransportCellularProfileOneOfPdnTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportCellularProfilePdnTypeDef


@dataclass
class TransportCellularProfileOneOfPdnTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportCellularProfileDefaultPdnTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class TransportCellularProfileOneOfSliceTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportCellularProfileOneOfSliceDifferentiatorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportCellularProfileNetworkSlicing:
    slice_differentiator: Optional[
        Union[
            TransportCellularProfileOneOfSliceDifferentiatorOptionsDef1,
            OneOfSliceDifferentiatorOptionsDef2,
            OneOfSliceDifferentiatorOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sliceDifferentiator"})
    slice_type: Optional[
        Union[
            TransportCellularProfileOneOfSliceTypeOptionsDef1,
            OneOfSliceTypeOptionsDef2,
            OneOfSliceTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sliceType"})


@dataclass
class TransportCellularProfileCommonCellularProfileInfoDef:
    apn: Union[TransportCellularProfileOneOfApnOptionsDef1, OneOfApnOptionsDef2]
    authentication: Optional[
        Union[TransportCellularProfileAuthentication1, TransportCellularProfileAuthentication2]
    ] = _field(default=None)
    network_slicing: Optional[TransportCellularProfileNetworkSlicing] = _field(
        default=None, metadata={"alias": "networkSlicing"}
    )
    no_overwrite: Optional[
        Union[OneOfNoOverwriteOptionsDef1, OneOfNoOverwriteOptionsDef2, OneOfNoOverwriteOptionsDef3]
    ] = _field(default=None, metadata={"alias": "noOverwrite"})
    pdn_type: Optional[
        Union[
            TransportCellularProfileOneOfPdnTypeOptionsDef1,
            OneOfPdnTypeOptionsDef2,
            TransportCellularProfileOneOfPdnTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class TransportCellularProfileProfileConfig:
    id: Union[TransportCellularProfileOneOfIdOptionsDef1, OneOfIdOptionsDef2]
    profile_info: TransportCellularProfileCommonCellularProfileInfoDef = _field(
        metadata={"alias": "profileInfo"}
    )


@dataclass
class TransportCellularProfileNonEsimCellularProfileConfigDef:
    """
    Regular Cellular profile (non-eSim) config
    """

    config_type: ConfigType = _field(metadata={"alias": "configType"})
    profile_config: TransportCellularProfileProfileConfig = _field(
        metadata={"alias": "profileConfig"}
    )


@dataclass
class EditCellularProfileProfileParcelForTransportPutRequest:
    """
    CellularProfile profile parcel schema for PUT request
    """

    data: TransportCellularProfileNonEsimCellularProfileConfigDef
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
