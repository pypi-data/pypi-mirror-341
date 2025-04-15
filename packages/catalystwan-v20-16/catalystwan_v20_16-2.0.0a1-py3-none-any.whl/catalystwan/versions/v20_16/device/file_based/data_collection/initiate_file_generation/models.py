# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field


@dataclass
class InitiateFileGenerationRequest:
    # UUID of the device
    device_uuid: str = _field(metadata={"alias": "deviceUUID"})
    requested_file_format: str = _field(metadata={"alias": "requestedFileFormat"})
    stats_command: str = _field(metadata={"alias": "statsCommand"})
