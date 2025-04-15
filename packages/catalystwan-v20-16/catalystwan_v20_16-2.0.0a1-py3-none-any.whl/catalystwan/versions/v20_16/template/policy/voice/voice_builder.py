# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceModel

if TYPE_CHECKING:
    from .definition.definition_builder import DefinitionBuilder
    from .devices.devices_builder import DevicesBuilder
    from .summary.summary_builder import SummaryBuilder


class VoiceBuilder:
    """
    Builds and executes requests for operations under /template/policy/voice
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Create Template
        POST /dataservice/template/policy/voice

        :param payload: Policy template
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/voice", payload=payload, **kw
        )

    def put(self, policy_id: str, payload: Any, **kw) -> Any:
        """
        Edit Template
        PUT /dataservice/template/policy/voice/{policyId}

        :param policy_id: Policy Id
        :param payload: Policy template
        :returns: Any
        """
        params = {
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/policy/voice/{policyId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, policy_id: str, **kw):
        """
        Delete Template
        DELETE /dataservice/template/policy/voice/{policyId}

        :param policy_id: Policy Id
        :returns: None
        """
        params = {
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/template/policy/voice/{policyId}", params=params, **kw
        )

    @overload
    def get(self, device_model: DeviceModel, **kw) -> List[Any]:
        """
        Get templates that map a device model
        GET /dataservice/template/policy/voice/{deviceModel}

        :param device_model: Device model
        :returns: List[Any]
        """
        ...

    @overload
    def get(self, **kw) -> List[Any]:
        """
        Generate template list
        GET /dataservice/template/policy/voice

        :returns: List[Any]
        """
        ...

    def get(self, device_model: Optional[DeviceModel] = None, **kw) -> List[Any]:
        # /dataservice/template/policy/voice/{deviceModel}
        if self._request_adapter.param_checker([(device_model, DeviceModel)], []):
            params = {
                "deviceModel": device_model,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/template/policy/voice/{deviceModel}",
                return_type=List[Any],
                params=params,
                **kw,
            )
        # /dataservice/template/policy/voice
        if self._request_adapter.param_checker([], [device_model]):
            return self._request_adapter.request(
                "GET", "/dataservice/template/policy/voice", return_type=List[Any], **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def definition(self) -> DefinitionBuilder:
        """
        The definition property
        """
        from .definition.definition_builder import DefinitionBuilder

        return DefinitionBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
