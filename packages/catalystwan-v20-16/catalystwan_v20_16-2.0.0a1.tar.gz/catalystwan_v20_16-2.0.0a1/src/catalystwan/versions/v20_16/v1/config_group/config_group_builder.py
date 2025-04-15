# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    ConfigGroup,
    CreateConfigGroupPostRequest,
    CreateConfigGroupPostResponse,
    EditConfigGroupPutRequest,
    EditConfigGroupPutResponse,
)

if TYPE_CHECKING:
    from .device.device_builder import DeviceBuilder
    from .rules.rules_builder import RulesBuilder


class ConfigGroupBuilder:
    """
    Builds and executes requests for operations under /v1/config-group
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: CreateConfigGroupPostRequest, **kw) -> CreateConfigGroupPostResponse:
        """
        Create a new Configuration Group
        POST /dataservice/v1/config-group

        :param payload: Config Group
        :returns: CreateConfigGroupPostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/config-group",
            return_type=CreateConfigGroupPostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, config_group_id: str, payload: EditConfigGroupPutRequest, **kw
    ) -> EditConfigGroupPutResponse:
        """
        Edit a Configuration Group
        PUT /dataservice/v1/config-group/{configGroupId}

        :param config_group_id: Config group id
        :param payload: Config Group
        :returns: EditConfigGroupPutResponse
        """
        params = {
            "configGroupId": config_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/config-group/{configGroupId}",
            return_type=EditConfigGroupPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, config_group_id: str, delete_profiles: Optional[bool] = None, **kw):
        """
        Delete Config Group
        DELETE /dataservice/v1/config-group/{configGroupId}

        :param config_group_id: Config group id
        :param delete_profiles: Delete profiles
        :returns: None
        """
        params = {
            "configGroupId": config_group_id,
            "deleteProfiles": delete_profiles,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/v1/config-group/{configGroupId}", params=params, **kw
        )

    @overload
    def get(self, *, config_group_id: str, device_list: Optional[bool] = True, **kw) -> ConfigGroup:
        """
        Get a Configuration Group by ID
        GET /dataservice/v1/config-group/{configGroupId}

        :param config_group_id: Config group id
        :param device_list: Including associated devices list
        :returns: ConfigGroup
        """
        ...

    @overload
    def get(
        self, *, solution: Optional[str] = None, name: Optional[str] = None, **kw
    ) -> List[ConfigGroup]:
        """
        Get a Configuration Group by Solution
        GET /dataservice/v1/config-group

        :param solution: Solution
        :param name: Name
        :returns: List[ConfigGroup]
        """
        ...

    def get(
        self,
        *,
        solution: Optional[str] = None,
        name: Optional[str] = None,
        config_group_id: Optional[str] = None,
        device_list: Optional[bool] = None,
        **kw,
    ) -> Union[List[ConfigGroup], ConfigGroup]:
        # /dataservice/v1/config-group/{configGroupId}
        if self._request_adapter.param_checker([(config_group_id, str)], [solution, name]):
            params = {
                "configGroupId": config_group_id,
                "deviceList": device_list,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/config-group/{configGroupId}",
                return_type=ConfigGroup,
                params=params,
                **kw,
            )
        # /dataservice/v1/config-group
        if self._request_adapter.param_checker([], [config_group_id, device_list]):
            params = {
                "solution": solution,
                "name": name,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/config-group",
                return_type=List[ConfigGroup],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def rules(self) -> RulesBuilder:
        """
        The rules property
        """
        from .rules.rules_builder import RulesBuilder

        return RulesBuilder(self._request_adapter)
