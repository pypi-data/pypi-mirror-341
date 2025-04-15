# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

FileDownloadStatus = Literal["COMPLETED", "ERROR", "IN_PROGRESS", "NOT_STARTED", "STARTED"]

SessionStatus = Literal["IN_PROGRESS", "NOT_STARTED", "START", "STOP"]


@dataclass
class GetFileDownloadStatusRes:
    file_download_status: Optional[FileDownloadStatus] = _field(
        default=None, metadata={"alias": "fileDownloadStatus"}
    )
    session_status: Optional[SessionStatus] = _field(
        default=None, metadata={"alias": "sessionStatus"}
    )
