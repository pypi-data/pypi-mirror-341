# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

CloudTypeParam = Literal["AWS", "AWS_GOVCLOUD", "AZURE", "AZURE_GOVCLOUD", "GCP"]


@dataclass
class GetMapResponse:
    conn: Optional[str] = _field(default=None)
    dest_id: Optional[str] = _field(default=None, metadata={"alias": "destId"})
    dest_type: Optional[str] = _field(default=None, metadata={"alias": "destType"})
    src_id: Optional[str] = _field(default=None, metadata={"alias": "srcId"})
    src_type: Optional[str] = _field(default=None, metadata={"alias": "srcType"})


@dataclass
class Taskid:
    """
    Task id for polling status
    """

    id: Optional[str] = _field(default=None)


@dataclass
class PostMapRequestMapped:
    cgw_attachment: Optional[str] = _field(default=None, metadata={"alias": "cgwAttachment"})
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    dest_id: Optional[str] = _field(default=None, metadata={"alias": "destId"})
    dest_region: Optional[str] = _field(default=None, metadata={"alias": "destRegion"})
    dest_tag: Optional[str] = _field(default=None, metadata={"alias": "destTag"})
    dest_type: Optional[str] = _field(default=None, metadata={"alias": "destType"})
    region: Optional[str] = _field(default=None)
    source_region: Optional[str] = _field(default=None, metadata={"alias": "sourceRegion"})
    source_tag: Optional[str] = _field(default=None, metadata={"alias": "sourceTag"})
    src_id: Optional[str] = _field(default=None, metadata={"alias": "srcId"})
    src_type: Optional[str] = _field(default=None, metadata={"alias": "srcType"})
    tunnel_id: Optional[str] = _field(default=None, metadata={"alias": "tunnelId"})


@dataclass
class PostMapRequestConnMatrix:
    conn: str
    dest_id: str = _field(metadata={"alias": "destId"})
    dest_type: str = _field(metadata={"alias": "destType"})
    src_id: str = _field(metadata={"alias": "srcId"})
    src_type: str = _field(metadata={"alias": "srcType"})
    mapped: Optional[List[PostMapRequestMapped]] = _field(default=None)
    outstanding_mapping: Optional[List[PostMapRequestMapped]] = _field(
        default=None, metadata={"alias": "outstandingMapping"}
    )
    unmapped: Optional[List[PostMapRequestMapped]] = _field(default=None)


@dataclass
class PostMapRequest:
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    conn_matrix: Optional[List[PostMapRequestConnMatrix]] = _field(
        default=None, metadata={"alias": "connMatrix"}
    )
