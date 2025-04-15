# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

InterconnectTypeParam = Literal["EQUINIX", "MEGAPORT"]


@dataclass
class InlineResponse2003:
    configured_hostname: Optional[str] = _field(
        default=None, metadata={"alias": "configuredHostname"}
    )
    configured_system_ip: Optional[str] = _field(
        default=None, metadata={"alias": "configuredSystemIP"}
    )
    device_model: Optional[str] = _field(default=None, metadata={"alias": "deviceModel"})
    uuid: Optional[str] = _field(default=None)
