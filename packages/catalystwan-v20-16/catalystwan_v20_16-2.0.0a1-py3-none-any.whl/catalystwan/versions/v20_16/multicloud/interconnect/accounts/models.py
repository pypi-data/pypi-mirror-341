# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class InterconnectAccountAttCredentials:
    """
    AT&T Credential information.
    """

    # Client id of the AT&T Account.
    client_id: str = _field(metadata={"alias": "clientId"})
    # Client secret of the AT&T Account.
    client_secret: str = _field(metadata={"alias": "clientSecret"})


@dataclass
class InterconnectAccountEquinixCredentials:
    """
    Equinix Credential information.
    """

    # Client id of the Equinix Account.
    client_id: str = _field(metadata={"alias": "clientId"})
    # Client secret of the Equinix Account.
    client_secret: str = _field(metadata={"alias": "clientSecret"})


@dataclass
class InterconnectAccountMegaportCredentials:
    """
    Megaport Credential Information
    """

    # Password of the Megaport Account.
    password: str
    # Username of the Megaport Account.
    username: str


@dataclass
class InterconnectAccount:
    # AT&T Credential information.
    att_credentials: InterconnectAccountAttCredentials = _field(
        metadata={"alias": "attCredentials"}
    )
    edge_account_id: str = _field(metadata={"alias": "edgeAccountId"})
    edge_account_name: str = _field(metadata={"alias": "edgeAccountName"})
    edge_type: str = _field(metadata={"alias": "edgeType"})
    # Equinix Credential information.
    equinix_credentials: InterconnectAccountEquinixCredentials = _field(
        metadata={"alias": "equinixCredentials"}
    )
    # Megaport Credential Information
    megaport_credentials: InterconnectAccountMegaportCredentials = _field(
        metadata={"alias": "megaportCredentials"}
    )
    billing_provider_type: Optional[str] = _field(
        default=None, metadata={"alias": "billingProviderType"}
    )
    cred_type: Optional[str] = _field(default=None, metadata={"alias": "credType"})
    description: Optional[str] = _field(default=None)
    # List of regions
    region_list: Optional[List[str]] = _field(default=None, metadata={"alias": "regionList"})
