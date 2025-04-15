# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class CreateResponse:
    """
    Response from PxGrid node creation on ISE
    """

    node_name: Optional[str] = _field(default=None, metadata={"alias": "nodeName"})
    password: Optional[str] = _field(default=None)
    user_name: Optional[str] = _field(default=None, metadata={"alias": "userName"})


@dataclass
class CreateBody:
    """
    Body for PxGrid node create on ISE
    """

    node_name: Optional[str] = _field(default=None, metadata={"alias": "nodeName"})
