# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

ValueType = Literal["ARRAY", "FALSE", "NULL", "NUMBER", "OBJECT", "STRING", "TRUE"]


@dataclass
class SmartLicensingfetchAccountsRespVirtualAccounts:
    default: Optional[bool] = _field(default=None)
    name: Optional[str] = _field(default=None)
    virtual_account_id: Optional[str] = _field(default=None)


@dataclass
class SmartLicensingfetchAccountsResp:
    account_id: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
    virtual_accounts: Optional[List[SmartLicensingfetchAccountsRespVirtualAccounts]] = _field(
        default=None
    )


@dataclass
class FetchAccounts1PostRequest:
    empty: Optional[bool] = _field(default=None)
    value_type: Optional[ValueType] = _field(default=None, metadata={"alias": "valueType"})
