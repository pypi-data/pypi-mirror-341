# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

ConnectType = Literal["AWS", "AWSHC", "INTERCONNECT_ATTACHMENT", "PRIMARY", "SECONDARY"]

CloudType = Literal["AWS", "AWS_GOVCLOUD", "AZURE", "AZURE_GOVCLOUD", "GCP"]

EdgeType = Literal["EQUINIX", "MEGAPORT"]


@dataclass
class InterconnectPartnerPortsDetails:
    """
    Megaport specific partner port fields.
    """

    authorization_key: Optional[str] = _field(default=None, metadata={"alias": "authorizationKey"})
    # Megaport companyId for the region.
    company_uid: Optional[str] = _field(default=None, metadata={"alias": "companyUid"})
    connect_type: Optional[ConnectType] = _field(default=None, metadata={"alias": "connectType"})
    # Megaport id for the region.
    product_uid: Optional[str] = _field(default=None, metadata={"alias": "productUid"})
    # Bandwidth speeds supported at the region.
    speed: Optional[str] = _field(default=None)
    # Cross connect (VXC) id connected to the region
    vxc_id: Optional[str] = _field(default=None, metadata={"alias": "vxcId"})
    # Cross Connect enabled Megaport region.
    vxc_permitted: Optional[bool] = _field(default=None, metadata={"alias": "vxcPermitted"})


@dataclass
class InterconnectPartnerPorts:
    """
    Interconnect partner port information
    """

    # Megaport specific partner port fields.
    att_partner_port: Optional[InterconnectPartnerPortsDetails] = _field(
        default=None, metadata={"alias": "attPartnerPort"}
    )
    cloud_type: Optional[CloudType] = _field(default=None, metadata={"alias": "cloudType"})
    edge_type: Optional[EdgeType] = _field(default=None, metadata={"alias": "edgeType"})
    # Megaport specific partner port fields.
    eq_partner_port: Optional[InterconnectPartnerPortsDetails] = _field(
        default=None, metadata={"alias": "eqPartnerPort"}
    )
    location_id: Optional[str] = _field(default=None, metadata={"alias": "locationId"})
    # Megaport specific partner port fields.
    mp_partner_port: Optional[InterconnectPartnerPortsDetails] = _field(
        default=None, metadata={"alias": "mpPartnerPort"}
    )
    name: Optional[str] = _field(default=None)


@dataclass
class InlineResponse2006:
    edge_partner_ports_list: Optional[List[InterconnectPartnerPorts]] = _field(
        default=None, metadata={"alias": "edgePartnerPortsList"}
    )
