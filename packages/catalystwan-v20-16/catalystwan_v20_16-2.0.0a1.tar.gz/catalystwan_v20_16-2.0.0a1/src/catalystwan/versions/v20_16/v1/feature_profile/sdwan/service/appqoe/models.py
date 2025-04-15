# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

VirtualApplicationApplicationTypeDef = Literal["dreopt"]

VirtualApplicationResourceProfileDef = Literal["default", "extra-large", "large", "medium", "small"]

VariableOptionTypeDef = Literal["variable"]

DefaultVirtualApplicationResourceProfileDef = Literal["default"]

AppqoeDeviceRoleDef = Literal[
    "forwarder",
    "forwarderAndServiceNode",
    "forwarderAndServiceNodeWithDre",
    "serviceNode",
    "serviceNodeWithDre",
]

DefaultAppnavControllerGroupDef = Literal["ACG-APPQOE"]

DefaultServiceNodeGroupDef = Literal["SNG-APPQOE"]

AppnavControllerGroupAppnavControllersDefaultAddressDef = Literal["192.168.2.1"]

DefaultExternalServiceNodeAddressDef = Literal["192.168.2.2"]

DefaultExternalServiceNodeVpgIpDef = Literal["192.168.2.1/24"]


@dataclass
class OneOfDreoptOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDreoptOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfVirtualApplicationInstanceIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVirtualApplicationApplicationTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VirtualApplicationApplicationTypeDef


@dataclass
class OneOfVirtualApplicationResourceProfileOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VirtualApplicationResourceProfileDef


@dataclass
class OneOfVirtualApplicationResourceProfileOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVirtualApplicationResourceProfileOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultVirtualApplicationResourceProfileDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VirtualApplication:
    instance_id: OneOfVirtualApplicationInstanceIdOptionsDef = _field(
        metadata={"alias": "instanceId"}
    )
    application_type: Optional[OneOfVirtualApplicationApplicationTypeOptionsDef] = _field(
        default=None, metadata={"alias": "applicationType"}
    )
    resource_profile: Optional[
        Union[
            OneOfVirtualApplicationResourceProfileOptionsDef1,
            OneOfVirtualApplicationResourceProfileOptionsDef2,
            OneOfVirtualApplicationResourceProfileOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "resourceProfile"})


@dataclass
class OneOfAppqoeDeviceRoleOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AppqoeDeviceRoleDef


@dataclass
class OneOfAppqoeNameOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAppqoeAppnavControllerGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAppqoeServiceNodeGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceNodeGroups:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAppqoeEnableOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAppqoeVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAppqoeVpnOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAppqoeVpnOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Appqoe:
    name: OneOfAppqoeNameOptionsDef
    appnav_controller_group: Optional[OneOfAppqoeAppnavControllerGroupOptionsDef] = _field(
        default=None, metadata={"alias": "appnavControllerGroup"}
    )
    enable: Optional[OneOfAppqoeEnableOptionsDef] = _field(default=None)
    service_node_group: Optional[OneOfAppqoeServiceNodeGroupOptionsDef] = _field(
        default=None, metadata={"alias": "serviceNodeGroup"}
    )
    # Service node group
    service_node_groups: Optional[List[ServiceNodeGroups]] = _field(
        default=None, metadata={"alias": "serviceNodeGroups"}
    )
    vpn: Optional[
        Union[OneOfAppqoeVpnOptionsDef1, OneOfAppqoeVpnOptionsDef2, OneOfAppqoeVpnOptionsDef3]
    ] = _field(default=None)


@dataclass
class ServiceContext:
    """
    Service Context
    """

    # Appqoe
    appqoe: Optional[List[Appqoe]] = _field(default=None)


@dataclass
class Forwarder1:
    appnav_controller_group: Any = _field(metadata={"alias": "appnavControllerGroup"})
    service_node_group: Any = _field(metadata={"alias": "serviceNodeGroup"})
    # Service Context
    service_context: Optional[ServiceContext] = _field(
        default=None, metadata={"alias": "serviceContext"}
    )


@dataclass
class OneOfAppnavControllerGroupGroupNameOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultAppnavControllerGroupDef


@dataclass
class OneOfAppnavControllerGroupAppnavControllersAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[Any, str]


@dataclass
class OneOfAppnavControllerGroupAppnavControllersAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAppnavControllerGroupAppnavControllersVpnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AppnavControllers:
    address: Union[
        OneOfAppnavControllerGroupAppnavControllersAddressOptionsDef1,
        OneOfAppnavControllerGroupAppnavControllersAddressOptionsDef2,
    ]
    vpn: Optional[OneOfAppnavControllerGroupAppnavControllersVpnOptionsDef] = _field(default=None)


@dataclass
class AppnavControllerGroup:
    group_name: OneOfAppnavControllerGroupGroupNameOptionsDef = _field(
        metadata={"alias": "groupName"}
    )
    # List of controllers
    appnav_controllers: Optional[List[AppnavControllers]] = _field(
        default=None, metadata={"alias": "appnavControllers"}
    )


@dataclass
class OneOfServiceNodeGroupNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceNodeGroupNameOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultServiceNodeGroupDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDefaultFalseServiceNodeGroupInternalOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceNodeGroupServiceNodeAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[Any, str]


@dataclass
class ServiceNode:
    address: OneOfServiceNodeGroupServiceNodeAddressOptionsDef


@dataclass
class ServiceNodeGroup:
    name: Union[OneOfServiceNodeGroupNameOptionsDef1, OneOfServiceNodeGroupNameOptionsDef2]
    internal: Optional[OneOfDefaultFalseServiceNodeGroupInternalOptionsDef] = _field(default=None)
    # Service Node Information
    service_node: Optional[List[ServiceNode]] = _field(
        default=None, metadata={"alias": "serviceNode"}
    )


@dataclass
class Forwarder2:
    # Appnav controller group name
    appnav_controller_group: Optional[List[AppnavControllerGroup]] = _field(
        default=None, metadata={"alias": "appnavControllerGroup"}
    )
    # Service Context
    service_context: Optional[ServiceContext] = _field(
        default=None, metadata={"alias": "serviceContext"}
    )
    # Name
    service_node_group: Optional[List[ServiceNodeGroup]] = _field(
        default=None, metadata={"alias": "serviceNodeGroup"}
    )


@dataclass
class OneOfAppnavControllerGroupAppnavControllersDefaultAddressOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AppnavControllerGroupAppnavControllersDefaultAddressDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AppqoeAppnavControllers:
    address: OneOfAppnavControllerGroupAppnavControllersDefaultAddressOptionsDef


@dataclass
class AppqoeAppnavControllerGroup:
    group_name: OneOfAppnavControllerGroupGroupNameOptionsDef = _field(
        metadata={"alias": "groupName"}
    )
    # List of controllers
    appnav_controllers: Optional[List[AppqoeAppnavControllers]] = _field(
        default=None, metadata={"alias": "appnavControllers"}
    )


@dataclass
class OneOfDefaultServiceNodeGroupNameOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultServiceNodeGroupDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDefaultTrueServiceNodeGroupInternalOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDefaultExternalServiceNodeGroupServiceNodeAddressOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultExternalServiceNodeAddressDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AppqoeServiceNode:
    address: OneOfDefaultExternalServiceNodeGroupServiceNodeAddressOptionsDef


@dataclass
class AppqoeServiceNodeGroup:
    name: OneOfDefaultServiceNodeGroupNameOptionsDef
    internal: Optional[OneOfDefaultTrueServiceNodeGroupInternalOptionsDef] = _field(default=None)
    # Service Node Information
    service_node: Optional[List[AppqoeServiceNode]] = _field(
        default=None, metadata={"alias": "serviceNode"}
    )


@dataclass
class ForwarderAndServiceNode:
    """
    Appqoe Device Role Forwarder And ServiceNode
    """

    # Appnav controller group name
    appnav_controller_group: Optional[List[AppqoeAppnavControllerGroup]] = _field(
        default=None, metadata={"alias": "appnavControllerGroup"}
    )
    # Service Context
    service_context: Optional[ServiceContext] = _field(
        default=None, metadata={"alias": "serviceContext"}
    )
    # Name
    service_node_group: Optional[List[AppqoeServiceNodeGroup]] = _field(
        default=None, metadata={"alias": "serviceNodeGroup"}
    )


@dataclass
class OneOfServiceNodeGroupExternalNodeOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceNodeGroupServiceNodeVpgIpOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultExternalServiceNodeVpgIpDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanServiceAppqoeServiceNode:
    address: OneOfDefaultExternalServiceNodeGroupServiceNodeAddressOptionsDef
    vpg_ip: Optional[OneOfServiceNodeGroupServiceNodeVpgIpOptionsDef] = _field(
        default=None, metadata={"alias": "vpgIp"}
    )


@dataclass
class ServiceAppqoeServiceNodeGroup:
    name: OneOfDefaultServiceNodeGroupNameOptionsDef
    external_node: Optional[OneOfServiceNodeGroupExternalNodeOptionsDef] = _field(
        default=None, metadata={"alias": "externalNode"}
    )
    # Service Node Information
    service_node: Optional[List[SdwanServiceAppqoeServiceNode]] = _field(
        default=None, metadata={"alias": "serviceNode"}
    )


@dataclass
class ServiceAppqoeServiceNode:
    """
    Appqoe Device Role ServiceNode
    """

    # Name
    service_node_group: Optional[List[ServiceAppqoeServiceNodeGroup]] = _field(
        default=None, metadata={"alias": "serviceNodeGroup"}
    )


@dataclass
class AppqoeData:
    appqoe_device_role: OneOfAppqoeDeviceRoleOptionsDef = _field(
        metadata={"alias": "appqoeDeviceRole"}
    )
    dreopt: Optional[Union[OneOfDreoptOptionsDef1, OneOfDreoptOptionsDef2]] = _field(default=None)
    # Appqoe Device Role Forwarder
    forwarder: Optional[Union[Forwarder1, Forwarder2]] = _field(default=None)
    # Appqoe Device Role Forwarder And ServiceNode
    forwarder_and_service_node: Optional[ForwarderAndServiceNode] = _field(
        default=None, metadata={"alias": "forwarderAndServiceNode"}
    )
    # Appqoe Device Role ServiceNode
    service_node: Optional[ServiceAppqoeServiceNode] = _field(
        default=None, metadata={"alias": "serviceNode"}
    )
    # Virtual application Instance
    virtual_application: Optional[List[VirtualApplication]] = _field(
        default=None, metadata={"alias": "virtualApplication"}
    )


@dataclass
class Payload:
    """
    Appqoe profile feature schema for request
    """

    data: AppqoeData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class Data:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # Appqoe profile feature schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanServiceAppqoePayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateAppqoeProfileParcelForServicePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class V1FeatureProfileSdwanServiceAppqoeServiceNode:
    address: OneOfDefaultExternalServiceNodeGroupServiceNodeAddressOptionsDef
    vpg_ip: Optional[OneOfServiceNodeGroupServiceNodeVpgIpOptionsDef] = _field(
        default=None, metadata={"alias": "vpgIp"}
    )


@dataclass
class SdwanServiceAppqoeServiceNodeGroup:
    name: OneOfDefaultServiceNodeGroupNameOptionsDef
    external_node: Optional[OneOfServiceNodeGroupExternalNodeOptionsDef] = _field(
        default=None, metadata={"alias": "externalNode"}
    )
    # Service Node Information
    service_node: Optional[List[V1FeatureProfileSdwanServiceAppqoeServiceNode]] = _field(
        default=None, metadata={"alias": "serviceNode"}
    )


@dataclass
class FeatureProfileSdwanServiceAppqoeServiceNode:
    """
    Appqoe Device Role ServiceNode
    """

    # Name
    service_node_group: Optional[List[SdwanServiceAppqoeServiceNodeGroup]] = _field(
        default=None, metadata={"alias": "serviceNodeGroup"}
    )


@dataclass
class ServiceAppqoeData:
    appqoe_device_role: OneOfAppqoeDeviceRoleOptionsDef = _field(
        metadata={"alias": "appqoeDeviceRole"}
    )
    dreopt: Optional[Union[OneOfDreoptOptionsDef1, OneOfDreoptOptionsDef2]] = _field(default=None)
    # Appqoe Device Role Forwarder
    forwarder: Optional[Union[Forwarder1, Forwarder2]] = _field(default=None)
    # Appqoe Device Role Forwarder And ServiceNode
    forwarder_and_service_node: Optional[ForwarderAndServiceNode] = _field(
        default=None, metadata={"alias": "forwarderAndServiceNode"}
    )
    # Appqoe Device Role ServiceNode
    service_node: Optional[FeatureProfileSdwanServiceAppqoeServiceNode] = _field(
        default=None, metadata={"alias": "serviceNode"}
    )
    # Virtual application Instance
    virtual_application: Optional[List[VirtualApplication]] = _field(
        default=None, metadata={"alias": "virtualApplication"}
    )


@dataclass
class CreateAppqoeProfileParcelForServicePostRequest:
    """
    Appqoe profile feature schema for request
    """

    data: ServiceAppqoeData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanServiceAppqoePayload:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # Appqoe profile feature schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditAppqoeProfileParcelForServicePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceNode2:
    address: OneOfDefaultExternalServiceNodeGroupServiceNodeAddressOptionsDef
    vpg_ip: Optional[OneOfServiceNodeGroupServiceNodeVpgIpOptionsDef] = _field(
        default=None, metadata={"alias": "vpgIp"}
    )


@dataclass
class FeatureProfileSdwanServiceAppqoeServiceNodeGroup:
    name: OneOfDefaultServiceNodeGroupNameOptionsDef
    external_node: Optional[OneOfServiceNodeGroupExternalNodeOptionsDef] = _field(
        default=None, metadata={"alias": "externalNode"}
    )
    # Service Node Information
    service_node: Optional[List[ServiceNode2]] = _field(
        default=None, metadata={"alias": "serviceNode"}
    )


@dataclass
class ServiceNode1:
    """
    Appqoe Device Role ServiceNode
    """

    # Name
    service_node_group: Optional[List[FeatureProfileSdwanServiceAppqoeServiceNodeGroup]] = _field(
        default=None, metadata={"alias": "serviceNodeGroup"}
    )


@dataclass
class SdwanServiceAppqoeData:
    appqoe_device_role: OneOfAppqoeDeviceRoleOptionsDef = _field(
        metadata={"alias": "appqoeDeviceRole"}
    )
    dreopt: Optional[Union[OneOfDreoptOptionsDef1, OneOfDreoptOptionsDef2]] = _field(default=None)
    # Appqoe Device Role Forwarder
    forwarder: Optional[Union[Forwarder1, Forwarder2]] = _field(default=None)
    # Appqoe Device Role Forwarder And ServiceNode
    forwarder_and_service_node: Optional[ForwarderAndServiceNode] = _field(
        default=None, metadata={"alias": "forwarderAndServiceNode"}
    )
    # Appqoe Device Role ServiceNode
    service_node: Optional[ServiceNode1] = _field(default=None, metadata={"alias": "serviceNode"})
    # Virtual application Instance
    virtual_application: Optional[List[VirtualApplication]] = _field(
        default=None, metadata={"alias": "virtualApplication"}
    )


@dataclass
class EditAppqoeProfileParcelForServicePutRequest:
    """
    Appqoe profile feature schema for request
    """

    data: SdwanServiceAppqoeData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
