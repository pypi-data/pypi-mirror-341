# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

Value = Literal["crl", "crl none", "none"]

CertificateValue = Literal["none"]


@dataclass
class OneOfTrustpointNameOptionDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfCertificateUuidOptionDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Certificates:
    certificate_uuid: OneOfCertificateUuidOptionDef = _field(metadata={"alias": "certificateUUID"})
    trust_point_name: OneOfTrustpointNameOptionDef = _field(metadata={"alias": "trustPointName"})


@dataclass
class OneOfScepUrlOptionDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfScepPasswordOptionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfScepPasswordOptionDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfScepPasswordOptionDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVrfOptionsWithDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVrfOptionsWithDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVrfOptionsWithDefault3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSubjectNameOptionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSubjectNameOptionDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfCrlCheckOptionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCrlCheckOptionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CertificateValue  # pytype: disable=annotation-type-mismatch


@dataclass
class ScepCertificates:
    certificate_uuid: OneOfCertificateUuidOptionDef = _field(metadata={"alias": "certificateUUID"})
    crl_check: Union[OneOfCrlCheckOptionDef1, OneOfCrlCheckOptionDef2] = _field(
        metadata={"alias": "crlCheck"}
    )
    scep_url: OneOfScepUrlOptionDef = _field(metadata={"alias": "scepUrl"})
    subject_name: Union[OneOfSubjectNameOptionDef1, OneOfSubjectNameOptionDef2] = _field(
        metadata={"alias": "subjectName"}
    )
    trust_point_name: OneOfTrustpointNameOptionDef = _field(metadata={"alias": "trustPointName"})
    scep_password: Optional[
        Union[OneOfScepPasswordOptionDef1, OneOfScepPasswordOptionDef2, OneOfScepPasswordOptionDef3]
    ] = _field(default=None, metadata={"alias": "scepPassword"})
    scep_vrf: Optional[
        Union[OneOfVrfOptionsWithDefault1, OneOfVrfOptionsWithDefault2, OneOfVrfOptionsWithDefault3]
    ] = _field(default=None, metadata={"alias": "scepVrf"})


@dataclass
class Data1:
    # Thirdparty CA Certificate List
    certificates: List[Certificates]
    # Feature Certificates Enrollment through SCEP
    scep_certificates: Optional[List[ScepCertificates]] = _field(
        default=None, metadata={"alias": "scepCertificates"}
    )


@dataclass
class Data2:
    # Feature Certificates Enrollment through SCEP
    scep_certificates: List[ScepCertificates] = _field(metadata={"alias": "scepCertificates"})
    # Thirdparty CA Certificate List
    certificates: Optional[List[Certificates]] = _field(default=None)


@dataclass
class Payload:
    """
    Certificate feature schema
    """

    data: Union[Data1, Data2]
    name: str
    # Set the feature description
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
    # Certificate feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingSystemCertificatePayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingCertificateFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdroutingCertificateFeaturePostRequest:
    """
    Certificate feature schema
    """

    data: Union[Data1, Data2]
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingSystemCertificatePayload:
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
    # Certificate feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingCertificateFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditSdroutingCertificateFeaturePutRequest:
    """
    Certificate feature schema
    """

    data: Union[Data1, Data2]
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
