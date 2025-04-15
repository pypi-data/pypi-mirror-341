# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class GenerateDeviceStateDataData:
    _rid: Optional[int] = _field(default=None, metadata={"alias": "@rid"})
    auto_downstream_bandwidth: Optional[str] = _field(
        default=None, metadata={"alias": "auto-downstream-bandwidth"}
    )
    auto_upstream_bandwidth: Optional[str] = _field(
        default=None, metadata={"alias": "auto-upstream-bandwidth"}
    )
    bia_address: Optional[str] = _field(default=None, metadata={"alias": "bia-address"})
    create_time_stamp: Optional[str] = _field(default=None, metadata={"alias": "createTimeStamp"})
    description: Optional[str] = _field(default=None)
    hwaddr: Optional[str] = _field(default=None)
    if_admin_status: Optional[str] = _field(default=None, metadata={"alias": "if-admin-status"})
    if_oper_status: Optional[str] = _field(default=None, metadata={"alias": "if-oper-status"})
    ifindex: Optional[str] = _field(default=None)
    ifname: Optional[str] = _field(default=None)
    interface_type: Optional[str] = _field(default=None, metadata={"alias": "interface-type"})
    ip_address: Optional[str] = _field(default=None, metadata={"alias": "ip-address"})
    ipv4_subnet_mask: Optional[str] = _field(default=None, metadata={"alias": "ipv4-subnet-mask"})
    ipv4_tcp_adjust_mss: Optional[str] = _field(
        default=None, metadata={"alias": "ipv4-tcp-adjust-mss"}
    )
    ipv6_tcp_adjust_mss: Optional[str] = _field(
        default=None, metadata={"alias": "ipv6-tcp-adjust-mss"}
    )
    lastupdated: Optional[int] = _field(default=None)
    mtu: Optional[str] = _field(default=None)
    record_id: Optional[str] = _field(default=None, metadata={"alias": "recordId"})
    rx_drops: Optional[int] = _field(default=None, metadata={"alias": "rx-drops"})
    rx_errors: Optional[int] = _field(default=None, metadata={"alias": "rx-errors"})
    rx_octets: Optional[int] = _field(default=None, metadata={"alias": "rx-octets"})
    rx_packets: Optional[str] = _field(default=None, metadata={"alias": "rx-packets"})
    speed_mbps: Optional[str] = _field(default=None, metadata={"alias": "speed-mbps"})
    tx_drops: Optional[int] = _field(default=None, metadata={"alias": "tx-drops"})
    tx_errors: Optional[int] = _field(default=None, metadata={"alias": "tx-errors"})
    tx_octets: Optional[int] = _field(default=None, metadata={"alias": "tx-octets"})
    tx_packets: Optional[int] = _field(default=None, metadata={"alias": "tx-packets"})
    vdevice_data_key: Optional[str] = _field(default=None, metadata={"alias": "vdevice-dataKey"})
    vdevice_host_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-host-name"})
    vdevice_name: Optional[str] = _field(default=None, metadata={"alias": "vdevice-name"})
    vmanage_system_ip: Optional[str] = _field(default=None, metadata={"alias": "vmanage-system-ip"})
    vpn_id: Optional[str] = _field(default=None, metadata={"alias": "vpn-id"})


@dataclass
class GenerateDeviceStateData:
    data: Optional[List[GenerateDeviceStateDataData]] = _field(default=None)
