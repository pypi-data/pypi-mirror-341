# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

DefaultAuthenticationDef = Literal["none"]

AuthenticationDef = Literal["chap", "pap", "pap_chap"]

VariableOptionTypeDef = Literal["variable"]

PdnTypeDef = Literal["ipv4", "ipv4v6", "ipv6"]

DefaultPdnTypeDef = Literal["ipv4"]

EsimcellularProfileDefaultAuthenticationDef = Literal["none"]

EsimcellularProfileAuthenticationDef = Literal["chap", "pap", "pap_chap"]

EsimcellularProfilePdnTypeDef = Literal["ipv4", "ipv4v6", "ipv6"]

EsimcellularProfileDefaultPdnTypeDef = Literal["ipv4"]

TransportEsimcellularProfileDefaultAuthenticationDef = Literal["none"]

TransportEsimcellularProfileAuthenticationDef = Literal["chap", "pap", "pap_chap"]

TransportEsimcellularProfilePdnTypeDef = Literal["ipv4", "ipv4v6", "ipv6"]

TransportEsimcellularProfileDefaultPdnTypeDef = Literal["ipv4"]


@dataclass
class OneOfApnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


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
class CommonCellularProfileInfoDef:
    apn: OneOfApnOptionsDef
    authentication: Optional[Union[Authentication1, Authentication2]] = _field(default=None)
    no_overwrite: Optional[
        Union[OneOfNoOverwriteOptionsDef1, OneOfNoOverwriteOptionsDef2, OneOfNoOverwriteOptionsDef3]
    ] = _field(default=None, metadata={"alias": "noOverwrite"})
    pdn_type: Optional[
        Union[OneOfPdnTypeOptionsDef1, OneOfPdnTypeOptionsDef2, OneOfPdnTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class AccountId:
    """
    Set provider account Id used for this profile
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CommPlan:
    """
    Set communication plan used for this profile
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RatePlan:
    """
    Set rate plan used for this profile
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ESimAccountInfoDef:
    # Set provider account Id used for this profile
    account_id: AccountId = _field(metadata={"alias": "accountId"})
    # Set communication plan used for this profile
    comm_plan: CommPlan = _field(metadata={"alias": "commPlan"})
    # Set rate plan used for this profile
    rate_plan: RatePlan = _field(metadata={"alias": "ratePlan"})


@dataclass
class EsimCellularProfileConfigDef:
    """
    eSim Cellular profile config
    """

    account_info: ESimAccountInfoDef = _field(metadata={"alias": "accountInfo"})
    profile_info: CommonCellularProfileInfoDef = _field(metadata={"alias": "profileInfo"})


@dataclass
class Payload:
    """
    eSim CellularProfile feature schema for POST request
    """

    # eSim Cellular profile config
    data: EsimCellularProfileConfigDef
    name: str
    # Set the eSim CellularProfile feature description
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
    # eSim CellularProfile feature schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportEsimcellularProfilePayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateEsimCellularProfileProfileFeatureForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateEsimCellularProfileProfileFeatureForTransportPostRequest:
    """
    eSim CellularProfile feature schema for POST request
    """

    # eSim Cellular profile config
    data: EsimCellularProfileConfigDef
    name: str
    # Set the eSim CellularProfile feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EsimcellularProfileOneOfApnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EsimcellularProfileOneOfDefaultAuthenticationOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EsimcellularProfileDefaultAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EsimcellularProfileAuthentication1:
    no_authentication: EsimcellularProfileOneOfDefaultAuthenticationOptionsDef = _field(
        metadata={"alias": "noAuthentication"}
    )


@dataclass
class EsimcellularProfileOneOfAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EsimcellularProfileAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EsimcellularProfileOneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EsimcellularProfileOneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EsimcellularProfileNeedAuthentication:
    password: Union[EsimcellularProfileOneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    type_: Union[
        EsimcellularProfileOneOfAuthenticationOptionsDef1, OneOfAuthenticationOptionsDef2
    ] = _field(metadata={"alias": "type"})
    username: Union[EsimcellularProfileOneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class EsimcellularProfileAuthentication2:
    need_authentication: EsimcellularProfileNeedAuthentication = _field(
        metadata={"alias": "needAuthentication"}
    )


@dataclass
class EsimcellularProfileOneOfPdnTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EsimcellularProfilePdnTypeDef


@dataclass
class EsimcellularProfileOneOfPdnTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EsimcellularProfileDefaultPdnTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EsimcellularProfileCommonCellularProfileInfoDef:
    apn: EsimcellularProfileOneOfApnOptionsDef
    authentication: Optional[
        Union[EsimcellularProfileAuthentication1, EsimcellularProfileAuthentication2]
    ] = _field(default=None)
    no_overwrite: Optional[
        Union[OneOfNoOverwriteOptionsDef1, OneOfNoOverwriteOptionsDef2, OneOfNoOverwriteOptionsDef3]
    ] = _field(default=None, metadata={"alias": "noOverwrite"})
    pdn_type: Optional[
        Union[
            EsimcellularProfileOneOfPdnTypeOptionsDef1,
            OneOfPdnTypeOptionsDef2,
            EsimcellularProfileOneOfPdnTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class EsimcellularProfileESimAccountInfoDef:
    # Set provider account Id used for this profile
    account_id: AccountId = _field(metadata={"alias": "accountId"})
    # Set communication plan used for this profile
    comm_plan: CommPlan = _field(metadata={"alias": "commPlan"})
    # Set rate plan used for this profile
    rate_plan: RatePlan = _field(metadata={"alias": "ratePlan"})


@dataclass
class EsimcellularProfileEsimCellularProfileConfigDef:
    """
    eSim Cellular profile config
    """

    account_info: EsimcellularProfileESimAccountInfoDef = _field(metadata={"alias": "accountInfo"})
    profile_info: EsimcellularProfileCommonCellularProfileInfoDef = _field(
        metadata={"alias": "profileInfo"}
    )


@dataclass
class EsimcellularProfilePayload:
    """
    eSim CellularProfile feature schema for PUT request
    """

    # eSim Cellular profile config
    data: EsimcellularProfileEsimCellularProfileConfigDef
    name: str
    # Set the eSim CellularProfile feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanTransportEsimcellularProfilePayload:
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
    # eSim CellularProfile feature schema for PUT request
    payload: Optional[EsimcellularProfilePayload] = _field(default=None)


@dataclass
class EditEsimCellularProfileProfileFeatureForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportEsimcellularProfileOneOfApnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportEsimcellularProfileOneOfDefaultAuthenticationOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportEsimcellularProfileDefaultAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class TransportEsimcellularProfileAuthentication1:
    no_authentication: TransportEsimcellularProfileOneOfDefaultAuthenticationOptionsDef = _field(
        metadata={"alias": "noAuthentication"}
    )


@dataclass
class TransportEsimcellularProfileOneOfAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportEsimcellularProfileAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class TransportEsimcellularProfileOneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportEsimcellularProfileOneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportEsimcellularProfileNeedAuthentication:
    password: Union[TransportEsimcellularProfileOneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    type_: Union[
        TransportEsimcellularProfileOneOfAuthenticationOptionsDef1, OneOfAuthenticationOptionsDef2
    ] = _field(metadata={"alias": "type"})
    username: Union[TransportEsimcellularProfileOneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class TransportEsimcellularProfileAuthentication2:
    need_authentication: TransportEsimcellularProfileNeedAuthentication = _field(
        metadata={"alias": "needAuthentication"}
    )


@dataclass
class TransportEsimcellularProfileOneOfPdnTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportEsimcellularProfilePdnTypeDef


@dataclass
class TransportEsimcellularProfileOneOfPdnTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportEsimcellularProfileDefaultPdnTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class TransportEsimcellularProfileCommonCellularProfileInfoDef:
    apn: TransportEsimcellularProfileOneOfApnOptionsDef
    authentication: Optional[
        Union[
            TransportEsimcellularProfileAuthentication1, TransportEsimcellularProfileAuthentication2
        ]
    ] = _field(default=None)
    no_overwrite: Optional[
        Union[OneOfNoOverwriteOptionsDef1, OneOfNoOverwriteOptionsDef2, OneOfNoOverwriteOptionsDef3]
    ] = _field(default=None, metadata={"alias": "noOverwrite"})
    pdn_type: Optional[
        Union[
            TransportEsimcellularProfileOneOfPdnTypeOptionsDef1,
            OneOfPdnTypeOptionsDef2,
            TransportEsimcellularProfileOneOfPdnTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class TransportEsimcellularProfileESimAccountInfoDef:
    # Set provider account Id used for this profile
    account_id: AccountId = _field(metadata={"alias": "accountId"})
    # Set communication plan used for this profile
    comm_plan: CommPlan = _field(metadata={"alias": "commPlan"})
    # Set rate plan used for this profile
    rate_plan: RatePlan = _field(metadata={"alias": "ratePlan"})


@dataclass
class TransportEsimcellularProfileEsimCellularProfileConfigDef:
    """
    eSim Cellular profile config
    """

    account_info: TransportEsimcellularProfileESimAccountInfoDef = _field(
        metadata={"alias": "accountInfo"}
    )
    profile_info: TransportEsimcellularProfileCommonCellularProfileInfoDef = _field(
        metadata={"alias": "profileInfo"}
    )


@dataclass
class EditEsimCellularProfileProfileFeatureForTransportPutRequest:
    """
    eSim CellularProfile feature schema for PUT request
    """

    # eSim Cellular profile config
    data: TransportEsimcellularProfileEsimCellularProfileConfigDef
    name: str
    # Set the eSim CellularProfile feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
