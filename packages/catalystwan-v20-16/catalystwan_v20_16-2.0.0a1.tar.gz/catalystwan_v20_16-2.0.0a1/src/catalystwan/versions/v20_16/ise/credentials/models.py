# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class IseServer:
    ise_server_ip: str = _field(metadata={"alias": "iseServerIP"})
    password: str
    sgt: str
    user_and_user_group: str = _field(metadata={"alias": "userAndUserGroup"})
    user_name: str = _field(metadata={"alias": "userName"})
    vpn: str
    active_directory_domain: Optional[str] = _field(
        default=None, metadata={"alias": "activeDirectoryDomain"}
    )
    ise_cert_name: Optional[str] = _field(default=None, metadata={"alias": "iseCertName"})
    ise_root_cert: Optional[str] = _field(default=None, metadata={"alias": "iseRootCert"})
    join_point: Optional[str] = _field(default=None, metadata={"alias": "joinPoint"})
    px_grid_cert_name: Optional[str] = _field(default=None, metadata={"alias": "pxGridCertName"})
    px_grid_root_cert: Optional[str] = _field(default=None, metadata={"alias": "pxGridRootCert"})
