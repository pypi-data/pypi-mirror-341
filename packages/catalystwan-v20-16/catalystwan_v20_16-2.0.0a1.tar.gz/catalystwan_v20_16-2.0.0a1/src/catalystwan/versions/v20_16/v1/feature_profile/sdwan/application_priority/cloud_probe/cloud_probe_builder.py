# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class CloudProbeBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/cloud-probe
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, application_priority_id: str, cloud_probe_id: str, **kw) -> str:
        """
        Get Cloud Probe Profile Parcel by parcelId for application-priority feature profile
        GET /dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/cloud-probe/{cloudProbeId}

        :param application_priority_id: Feature Profile ID
        :param cloud_probe_id: Profile Parcel ID
        :returns: str
        """
        params = {
            "applicationPriorityId": application_priority_id,
            "cloudProbeId": cloud_probe_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sdwan/application-priority/{applicationPriorityId}/cloud-probe/{cloudProbeId}",
            return_type=str,
            params=params,
            **kw,
        )
