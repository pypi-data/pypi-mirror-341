# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import FeatureParam

if TYPE_CHECKING:
    from .cli.cli_builder import CliBuilder
    from .config.config_builder import ConfigBuilder
    from .feature.feature_builder import FeatureBuilder
    from .featuretemplates.featuretemplates_builder import FeaturetemplatesBuilder
    from .is_migration_required.is_migration_required_builder import IsMigrationRequiredBuilder
    from .migration.migration_builder import MigrationBuilder
    from .migration_info.migration_info_builder import MigrationInfoBuilder
    from .object.object_builder import ObjectBuilder
    from .resource_group.resource_group_builder import ResourceGroupBuilder
    from .syncstatus.syncstatus_builder import SyncstatusBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /template/device
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, feature: FeatureParam, **kw) -> List[Any]:
        """
        Generate template list


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/device

        :param feature: Feature
        :returns: List[Any]
        """
        params = {
            "feature": feature,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/device", return_type=List[Any], params=params, **kw
        )

    def put(self, template_id: str, payload: Any, **kw) -> Any:
        """
        Edit template


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        PUT /dataservice/template/device/{templateId}

        :param template_id: Template Id
        :param payload: Template
        :returns: Any
        """
        params = {
            "templateId": template_id,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/template/device/{templateId}", params=params, payload=payload, **kw
        )

    def delete(self, template_id: str, **kw):
        """
        Delete template


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        DELETE /dataservice/template/device/{templateId}

        :param template_id: Template Id
        :returns: None
        """
        params = {
            "templateId": template_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/template/device/{templateId}", params=params, **kw
        )

    @property
    def cli(self) -> CliBuilder:
        """
        The cli property
        """
        from .cli.cli_builder import CliBuilder

        return CliBuilder(self._request_adapter)

    @property
    def config(self) -> ConfigBuilder:
        """
        The config property
        """
        from .config.config_builder import ConfigBuilder

        return ConfigBuilder(self._request_adapter)

    @property
    def feature(self) -> FeatureBuilder:
        """
        The feature property
        """
        from .feature.feature_builder import FeatureBuilder

        return FeatureBuilder(self._request_adapter)

    @property
    def featuretemplates(self) -> FeaturetemplatesBuilder:
        """
        The featuretemplates property
        """
        from .featuretemplates.featuretemplates_builder import FeaturetemplatesBuilder

        return FeaturetemplatesBuilder(self._request_adapter)

    @property
    def is_migration_required(self) -> IsMigrationRequiredBuilder:
        """
        The is_migration_required property
        """
        from .is_migration_required.is_migration_required_builder import IsMigrationRequiredBuilder

        return IsMigrationRequiredBuilder(self._request_adapter)

    @property
    def migration(self) -> MigrationBuilder:
        """
        The migration property
        """
        from .migration.migration_builder import MigrationBuilder

        return MigrationBuilder(self._request_adapter)

    @property
    def migration_info(self) -> MigrationInfoBuilder:
        """
        The migration_info property
        """
        from .migration_info.migration_info_builder import MigrationInfoBuilder

        return MigrationInfoBuilder(self._request_adapter)

    @property
    def object(self) -> ObjectBuilder:
        """
        The object property
        """
        from .object.object_builder import ObjectBuilder

        return ObjectBuilder(self._request_adapter)

    @property
    def resource_group(self) -> ResourceGroupBuilder:
        """
        The resource-group property
        """
        from .resource_group.resource_group_builder import ResourceGroupBuilder

        return ResourceGroupBuilder(self._request_adapter)

    @property
    def syncstatus(self) -> SyncstatusBuilder:
        """
        The syncstatus property
        """
        from .syncstatus.syncstatus_builder import SyncstatusBuilder

        return SyncstatusBuilder(self._request_adapter)
