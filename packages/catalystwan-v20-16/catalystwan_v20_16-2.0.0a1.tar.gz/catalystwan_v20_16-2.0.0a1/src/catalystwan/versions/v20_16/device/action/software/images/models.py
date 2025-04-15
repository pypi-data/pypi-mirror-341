# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class Image:
    """
    This is the valid Image type
    """

    image: Optional[str] = _field(default=None)
