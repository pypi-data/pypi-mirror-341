# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceReachableData:
    available_versions: Optional[List[str]] = _field(
        default=None, metadata={"alias": "availableVersions"}
    )
    board_serial: Optional[int] = _field(default=None, metadata={"alias": "board-serial"})
    board_type: Optional[str] = _field(default=None)
    bootloader_version: Optional[str] = _field(default=None)
    build_number: Optional[int] = _field(default=None)
    certificate_not_valid_after: Optional[str] = _field(
        default=None, metadata={"alias": "certificate-not-valid-after"}
    )
    certificate_not_valid_before: Optional[str] = _field(
        default=None, metadata={"alias": "certificate-not-valid-before"}
    )
    certificate_status: Optional[str] = _field(
        default=None, metadata={"alias": "certificate-status"}
    )
    certificate_validity: Optional[str] = _field(
        default=None, metadata={"alias": "certificate-validity"}
    )
    chassis_number: Optional[str] = _field(default=None, metadata={"alias": "chassis-number"})
    chassis_serial_number: Optional[int] = _field(
        default=None, metadata={"alias": "chassis-serial-number"}
    )
    connected_v_manages: Optional[List[str]] = _field(
        default=None, metadata={"alias": "connectedVManages"}
    )
    control_connections: Optional[int] = _field(
        default=None, metadata={"alias": "controlConnections"}
    )
    control_connections_down: Optional[int] = _field(
        default=None, metadata={"alias": "controlConnectionsDown"}
    )
    control_connections_up: Optional[int] = _field(
        default=None, metadata={"alias": "controlConnectionsUp"}
    )
    cpu_load_display: Optional[int] = _field(default=None, metadata={"alias": "cpuLoadDisplay"})
    cpu_state: Optional[str] = _field(default=None, metadata={"alias": "cpuState"})
    default_version: Optional[str] = _field(default=None, metadata={"alias": "defaultVersion"})
    device_category: Optional[str] = _field(default=None, metadata={"alias": "device-category"})
    device_groups: Optional[List[str]] = _field(default=None, metadata={"alias": "device-groups"})
    device_id: Optional[str] = _field(default=None, metadata={"alias": "deviceId"})
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_os: Optional[str] = _field(default=None, metadata={"alias": "device-os"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    domain_id: Optional[int] = _field(default=None, metadata={"alias": "domain-id"})
    expected_control_connections: Optional[int] = _field(
        default=None, metadata={"alias": "expectedControlConnections"}
    )
    fips_mode: Optional[str] = _field(default=None)
    firmware_available_packages: Optional[List[str]] = _field(
        default=None, metadata={"alias": "firmwareAvailablePackages"}
    )
    firmware_available_versions: Optional[List[str]] = _field(
        default=None, metadata={"alias": "firmwareAvailableVersions"}
    )
    firmware_version: Optional[str] = _field(default=None, metadata={"alias": "firmwareVersion"})
    grid: Optional[int] = _field(default=None)
    group_id: Optional[List[str]] = _field(default=None, metadata={"alias": "groupId"})
    hardware_state: Optional[str] = _field(default=None, metadata={"alias": "hardwareState"})
    has_geo_data: Optional[bool] = _field(default=None, metadata={"alias": "hasGeoData"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    is_device_geo_data: Optional[bool] = _field(default=None, metadata={"alias": "isDeviceGeoData"})
    last_data_sync_time: Optional[int] = _field(
        default=None, metadata={"alias": "lastDataSyncTime"}
    )
    lastupdated: Optional[int] = _field(default=None)
    latitude: Optional[str] = _field(default=None)
    layout_level: Optional[int] = _field(default=None, metadata={"alias": "layoutLevel"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    longitude: Optional[str] = _field(default=None)
    mem_statenormal: Optional[str] = _field(default=None, metadata={"alias": "memStatenormal"})
    mem_usage: Optional[int] = _field(default=None, metadata={"alias": "memUsage"})
    mem_usage_display: Optional[int] = _field(default=None, metadata={"alias": "memUsageDisplay"})
    model_sku: Optional[str] = _field(default=None)
    mp_peers: Optional[int] = _field(default=None, metadata={"alias": "mpPeers"})
    name: Optional[str] = _field(default=None)
    number_vbond_peers: Optional[int] = _field(
        default=None, metadata={"alias": "number-vbond-peers"}
    )
    number_vsmart_control_connections: Optional[int] = _field(
        default=None, metadata={"alias": "number-vsmart-control-connections"}
    )
    number_vsmart_peers: Optional[int] = _field(
        default=None, metadata={"alias": "number-vsmart-peers"}
    )
    omp_peers_down: Optional[int] = _field(default=None, metadata={"alias": "ompPeersDown"})
    omp_peers_up: Optional[int] = _field(default=None, metadata={"alias": "ompPeersUp"})
    organization_name: Optional[str] = _field(default=None, metadata={"alias": "organization-name"})
    personality: Optional[str] = _field(default=None)
    platform: Optional[str] = _field(default=None)
    policy_template_nam: Optional[str] = _field(
        default=None, metadata={"alias": "policy-template-nam"}
    )
    policy_template_name: Optional[str] = _field(
        default=None, metadata={"alias": "policy-template-name"}
    )
    policy_template_version: Optional[str] = _field(
        default=None, metadata={"alias": "policy-template-version"}
    )
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[int] = _field(default=None, metadata={"alias": "site-id"})
    sp_organization_name: Optional[str] = _field(
        default=None, metadata={"alias": "sp-organization-name"}
    )
    state: Optional[str] = _field(default=None)
    state_description: Optional[str] = _field(default=None)
    status: Optional[str] = _field(default=None)
    status_order: Optional[int] = _field(default=None, metadata={"alias": "statusOrder"})
    sync_completed: Optional[int] = _field(default=None, metadata={"alias": "syncCompleted"})
    sync_queued: Optional[int] = _field(default=None, metadata={"alias": "syncQueued"})
    sync_scheduled: Optional[int] = _field(default=None, metadata={"alias": "syncScheduled"})
    sync_state: Optional[str] = _field(default=None, metadata={"alias": "syncState"})
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    testbed_mode: Optional[bool] = _field(default=None)
    timezone: Optional[str] = _field(default=None)
    token: Optional[str] = _field(default=None)
    total_cpu_count: Optional[int] = _field(default=None)
    uptime: Optional[str] = _field(default=None)
    uptime_date: Optional[int] = _field(default=None, metadata={"alias": "uptime-date"})
    uuid: Optional[str] = _field(default=None)
    vbond: Optional[str] = _field(default=None)
    vedge_list_version: Optional[int] = _field(
        default=None, metadata={"alias": "vedge-list-version"}
    )
    version: Optional[str] = _field(default=None)
    vmanage_connection_state: Optional[str] = _field(
        default=None, metadata={"alias": "vmanageConnectionState"}
    )
    vmanage_system_ip: Optional[str] = _field(default=None, metadata={"alias": "vmanage-system-ip"})
    vsmart_list_version: Optional[int] = _field(
        default=None, metadata={"alias": "vsmart-list-version"}
    )
