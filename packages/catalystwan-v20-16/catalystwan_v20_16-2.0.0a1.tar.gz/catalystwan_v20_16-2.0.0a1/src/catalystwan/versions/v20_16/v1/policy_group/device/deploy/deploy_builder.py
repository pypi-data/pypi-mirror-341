# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeployPolicyGroupPostRequest, DeployPolicyGroupPostResponse


class DeployBuilder:
    """
    Builds and executes requests for operations under /v1/policy-group/{policyGroupId}/device/deploy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, policy_group_id: str, payload: DeployPolicyGroupPostRequest, **kw
    ) -> DeployPolicyGroupPostResponse:
        """
        deploy policy group to devices
        POST /dataservice/v1/policy-group/{policyGroupId}/device/deploy

        :param policy_group_id: Policy Group Id
        :param payload: Payload
        :returns: DeployPolicyGroupPostResponse
        """
        params = {
            "policyGroupId": policy_group_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/policy-group/{policyGroupId}/device/deploy",
            return_type=DeployPolicyGroupPostResponse,
            params=params,
            payload=payload,
            **kw,
        )
