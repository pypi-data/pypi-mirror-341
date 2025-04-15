# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

InterconnectTypeParam = Literal["EQUINIX", "MEGAPORT"]


@dataclass
class InlineResponse20012:
    # Device-Link metro speed
    dl_metro_bandwidth: Optional[int] = _field(default=None, metadata={"alias": "dlMetroBandwidth"})


@dataclass
class InterconnectDeviceLinkDeviceList:
    # Interface used on the Interconnect Gateway to connect to the Device-Link.
    device_interface_id: Optional[str] = _field(
        default=None, metadata={"alias": "deviceInterfaceId"}
    )
    # IP assigned to the Interconnect Gateway interface to connect to the Device-Link.
    device_intf_ip_address: Optional[str] = _field(
        default=None, metadata={"alias": "deviceIntfIpAddress"}
    )
    # Name of the Interconnect Gateway in the Device-Link.
    device_name: Optional[str] = _field(default=None, metadata={"alias": "deviceName"})
    # Uuid of Interconnect Gateway in the Device-Link.
    device_uuid: Optional[str] = _field(default=None, metadata={"alias": "deviceUuid"})
    # IP assigned to the loopback interface of the Interconnect Gateway to form SDWAN tunnel.
    egw_loop_back_cidr: Optional[str] = _field(default=None, metadata={"alias": "egwLoopBackCidr"})


@dataclass
class InterconnectDeviceLink:
    """
    Interconnect Device-Link Object
    """

    # Device-Link Bandwidth Input.
    bandwidth: str
    # Name of the Interconnect Device-Link.
    device_link_name: str = _field(metadata={"alias": "deviceLinkName"})
    edge_account_id: str = _field(metadata={"alias": "edgeAccountId"})
    edge_type: str = _field(metadata={"alias": "edgeType"})
    # Uuid of the Interconnect Device-Link
    device_link_uuid: Optional[str] = _field(default=None, metadata={"alias": "deviceLinkUuid"})
    # Subnet pool for Interconnect Gateway interfaces in the Device-Link.
    device_linksubnet: Optional[str] = _field(default=None, metadata={"alias": "deviceLinksubnet"})
    device_list: Optional[List[InterconnectDeviceLinkDeviceList]] = _field(
        default=None, metadata={"alias": "deviceList"}
    )
    # Device-Link Bandwidth at a given Metro.
    dl_metro_bandwidth: Optional[str] = _field(default=None, metadata={"alias": "dlMetroBandwidth"})
    edge_account_name: Optional[str] = _field(default=None, metadata={"alias": "edgeAccountName"})
    # Device-Link Bandwidth.
    link_bandwidth: Optional[str] = _field(default=None, metadata={"alias": "linkBandwidth"})
    resource_state: Optional[str] = _field(default=None, metadata={"alias": "resourceState"})
    resource_state_message: Optional[str] = _field(
        default=None, metadata={"alias": "resourceStateMessage"}
    )
    resource_state_update_ts: Optional[str] = _field(
        default=None, metadata={"alias": "resourceStateUpdateTs"}
    )
    # Subnet pool for Interconnect Gateway interfaces in the Device-Link.
    subnet: Optional[str] = _field(default=None)
    # Version of the payload.
    version: Optional[str] = _field(default=None)
