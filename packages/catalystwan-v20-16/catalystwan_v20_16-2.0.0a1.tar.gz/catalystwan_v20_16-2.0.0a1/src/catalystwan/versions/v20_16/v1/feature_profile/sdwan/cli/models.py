# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

ProfileType = Literal["cli"]

Solution = Literal["sdwan"]


@dataclass
class GetSdwanFeatureProfilesByFamilyAndTypeGetResponse:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    description: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    profile_id: Optional[str] = _field(default=None, metadata={"alias": "profileId"})
    profile_name: Optional[str] = _field(default=None, metadata={"alias": "profileName"})
    profile_type: Optional[ProfileType] = _field(default=None, metadata={"alias": "profileType"})
    solution: Optional[Solution] = _field(default=None)


@dataclass
class CreateSdwanFeatureProfilePostResponse:
    """
    Feature Profile POST Response schema
    """

    id: str


@dataclass
class FromFeatureProfileDef:
    copy: str


@dataclass
class CreateSdwanFeatureProfilePostRequest:
    """
    Feature Profile Schema for POST Request
    """

    description: str
    name: str
    from_feature_profile: Optional[FromFeatureProfileDef] = _field(
        default=None, metadata={"alias": "fromFeatureProfile"}
    )


@dataclass
class AssociatedProfileParcels:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    payload: Optional[Any] = _field(default=None)
    subparcels: Optional[List[Any]] = _field(default=None)


@dataclass
class GetSingleSdwanCliPayload:
    associated_profile_parcels: Optional[List[AssociatedProfileParcels]] = _field(
        default=None, metadata={"alias": "associatedProfileParcels"}
    )
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    description: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    profile_id: Optional[str] = _field(default=None, metadata={"alias": "profileId"})
    profile_name: Optional[str] = _field(default=None, metadata={"alias": "profileName"})
    profile_type: Optional[ProfileType] = _field(default=None, metadata={"alias": "profileType"})
    solution: Optional[Solution] = _field(default=None)


@dataclass
class EditSdwanFeatureProfilePutResponse:
    """
    Feature Profile PUT Response schema
    """

    id: str


@dataclass
class EditSdwanFeatureProfilePutRequest:
    """
    Feature Profile Schema for PUT Request
    """

    description: str
    name: str
