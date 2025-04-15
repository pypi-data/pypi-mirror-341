# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class PxGridInfo:
    """
    pxgrid information for making pxgrid api calls
    """

    px_grid_password: str = _field(metadata={"alias": "pxGridPassword"})
    px_grid_server_ip: str = _field(metadata={"alias": "pxGridServerIp"})
    px_grid_user_name: str = _field(metadata={"alias": "pxGridUserName"})
    status: str
    access_secret: Optional[str] = _field(default=None, metadata={"alias": "AccessSecret"})
    description: Optional[str] = _field(default=None)
    device_type: Optional[str] = _field(default=None, metadata={"alias": "deviceType"})
    node_name: Optional[str] = _field(default=None, metadata={"alias": "nodeName"})
    px_grid_host_name: Optional[str] = _field(default=None, metadata={"alias": "pxGridHostName"})
    rest_base_url: Optional[str] = _field(default=None, metadata={"alias": "restBaseURL"})
