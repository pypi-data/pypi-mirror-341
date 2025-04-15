# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

InterconnectTypeParam = Literal["EQUINIX", "MEGAPORT"]


@dataclass
class MulticloudSystemSettings:
    enable_monitoring: Optional[bool] = _field(default=None, metadata={"alias": "enableMonitoring"})
    # Enable or disable Configuration Group for Gateways
    use_configuration_group: Optional[str] = _field(
        default=None, metadata={"alias": "useConfigurationGroup"}
    )


@dataclass
class InterconnectGlobalSettings:
    bgp_asn: str = _field(metadata={"alias": "bgpAsn"})
    edge_gateway_solution: str = _field(metadata={"alias": "edgeGatewaySolution"})
    edge_type: str = _field(metadata={"alias": "edgeType"})
    instance_size: str = _field(metadata={"alias": "instanceSize"})
    loopback_cgw_color: str = _field(metadata={"alias": "loopbackCgwColor"})
    loopback_tunnel_color: str = _field(metadata={"alias": "loopbackTunnelColor"})
    software_image_id: str = _field(metadata={"alias": "softwareImageId"})
    invoice_reference: Optional[str] = _field(default=None, metadata={"alias": "invoiceReference"})
    ip_subnet_pool: Optional[str] = _field(default=None, metadata={"alias": "ipSubnetPool"})
    multicloud_system_settings: Optional[MulticloudSystemSettings] = _field(
        default=None, metadata={"alias": "multicloudSystemSettings"}
    )
