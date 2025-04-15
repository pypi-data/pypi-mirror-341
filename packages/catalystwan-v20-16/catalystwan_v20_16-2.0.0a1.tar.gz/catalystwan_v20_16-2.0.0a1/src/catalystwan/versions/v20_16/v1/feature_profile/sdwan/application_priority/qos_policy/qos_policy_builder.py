# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreatePolicyApplicationProfileParcelPostRequest,
    CreatePolicyApplicationProfileParcelPostResponse,
    EditPolicyApplicationProfileParcelPutRequest,
    EditPolicyApplicationProfileParcelPutResponse,
    GetSingleSdwanApplicationPriorityQosPolicyPayload,
)


class QosPolicyBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/qos-policy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        application_priority_id: str,
        payload: CreatePolicyApplicationProfileParcelPostRequest,
        **kw,
    ) -> CreatePolicyApplicationProfileParcelPostResponse:
        """
        Create QOS Policy feature for application-priority feature profile
        POST /dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/qos-policy

        :param application_priority_id: Application priority id
        :param payload: QOS Profile Parcel
        :returns: CreatePolicyApplicationProfileParcelPostResponse
        """
        params = {
            "applicationPriorityId": application_priority_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/qos-policy",
            return_type=CreatePolicyApplicationProfileParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(
        self, application_priority_id: str, qos_policy_id: str, **kw
    ) -> GetSingleSdwanApplicationPriorityQosPolicyPayload:
        """
        Get QOS Policy feature for application-priority feature profile
        GET /dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/qos-policy/{qosPolicyId}

        :param application_priority_id: Application priority id
        :param qos_policy_id: Qos policy id
        :returns: GetSingleSdwanApplicationPriorityQosPolicyPayload
        """
        params = {
            "applicationPriorityId": application_priority_id,
            "qosPolicyId": qos_policy_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/qos-policy/{qosPolicyId}",
            return_type=GetSingleSdwanApplicationPriorityQosPolicyPayload,
            params=params,
            **kw,
        )

    def put(
        self,
        application_priority_id: str,
        qos_policy_id: str,
        payload: EditPolicyApplicationProfileParcelPutRequest,
        **kw,
    ) -> EditPolicyApplicationProfileParcelPutResponse:
        """
        Edit QOS Policy feature for application-priority feature profile
        PUT /dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/qos-policy/{qosPolicyId}

        :param application_priority_id: Application priority id
        :param qos_policy_id: Qos policy id
        :param payload: QOS Profile Parcel
        :returns: EditPolicyApplicationProfileParcelPutResponse
        """
        params = {
            "applicationPriorityId": application_priority_id,
            "qosPolicyId": qos_policy_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/qos-policy/{qosPolicyId}",
            return_type=EditPolicyApplicationProfileParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, application_priority_id: str, qos_policy_id: str, **kw):
        """
        Delete QOS Policy feature for application-priority feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/qos-policy/{qosPolicyId}

        :param application_priority_id: Application priority id
        :param qos_policy_id: Qos policy id
        :returns: None
        """
        params = {
            "applicationPriorityId": application_priority_id,
            "qosPolicyId": qos_policy_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/qos-policy/{qosPolicyId}",
            params=params,
            **kw,
        )
