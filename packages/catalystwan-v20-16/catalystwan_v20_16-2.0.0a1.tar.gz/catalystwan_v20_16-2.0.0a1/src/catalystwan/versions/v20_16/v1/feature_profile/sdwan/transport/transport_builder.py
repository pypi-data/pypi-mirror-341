# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanTransportFeatureProfilePostRequest,
    CreateSdwanTransportFeatureProfilePostResponse,
    EditSdwanTransportFeatureProfilePutRequest,
    EditSdwanTransportFeatureProfilePutResponse,
    GetSdwanTransportFeatureProfilesGetResponse,
    GetSingleSdwanTransportPayload,
)

if TYPE_CHECKING:
    from .cellular_controller.cellular_controller_builder import CellularControllerBuilder
    from .cellular_profile.cellular_profile_builder import CellularProfileBuilder
    from .esimcellular_controller.esimcellular_controller_builder import (
        EsimcellularControllerBuilder,
    )
    from .esimcellular_profile.esimcellular_profile_builder import EsimcellularProfileBuilder
    from .gps.gps_builder import GpsBuilder
    from .ipv6_tracker.ipv6_tracker_builder import Ipv6TrackerBuilder
    from .ipv6_trackergroup.ipv6_trackergroup_builder import Ipv6TrackergroupBuilder
    from .management.management_builder import ManagementBuilder
    from .routing.routing_builder import RoutingBuilder
    from .t1_e1_controller.t1_e1_controller_builder import T1E1ControllerBuilder
    from .tracker.tracker_builder import TrackerBuilder
    from .trackergroup.trackergroup_builder import TrackergroupBuilder
    from .wan.wan_builder import WanBuilder


class TransportBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdwanTransportFeatureProfilePostRequest, **kw
    ) -> CreateSdwanTransportFeatureProfilePostResponse:
        """
        Create a SDWAN Transport Feature Profile
        POST /dataservice/v1/feature-profile/sdwan/transport

        :param payload: SDWAN Feature profile
        :returns: CreateSdwanTransportFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport",
            return_type=CreateSdwanTransportFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, transport_id: str, payload: EditSdwanTransportFeatureProfilePutRequest, **kw
    ) -> EditSdwanTransportFeatureProfilePutResponse:
        """
        Edit a SDWAN Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}

        :param transport_id: Feature Profile Id
        :param payload: SDWAN Feature profile
        :returns: EditSdwanTransportFeatureProfilePutResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}",
            return_type=EditSdwanTransportFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, **kw):
        """
        Delete Feature Profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}

        :param transport_id: Transport id
        :returns: None
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, *, transport_id: str, **kw) -> GetSingleSdwanTransportPayload:
        """
        Get a SDWAN Transport Feature Profile with transportId
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}

        :param transport_id: Feature Profile Id
        :returns: GetSingleSdwanTransportPayload
        """
        ...

    @overload
    def get(
        self, *, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetSdwanTransportFeatureProfilesGetResponse]:
        """
        Get all SDWAN Feature Profiles with giving Family and profile type
        GET /dataservice/v1/feature-profile/sdwan/transport

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetSdwanTransportFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        transport_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetSdwanTransportFeatureProfilesGetResponse], GetSingleSdwanTransportPayload]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}
        if self._request_adapter.param_checker([(transport_id, str)], [offset, limit]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}",
                return_type=GetSingleSdwanTransportPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport
        if self._request_adapter.param_checker([], [transport_id]):
            params = {
                "offset": offset,
                "limit": limit,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport",
                return_type=List[GetSdwanTransportFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def cellular_controller(self) -> CellularControllerBuilder:
        """
        The cellular-controller property
        """
        from .cellular_controller.cellular_controller_builder import CellularControllerBuilder

        return CellularControllerBuilder(self._request_adapter)

    @property
    def cellular_profile(self) -> CellularProfileBuilder:
        """
        The cellular-profile property
        """
        from .cellular_profile.cellular_profile_builder import CellularProfileBuilder

        return CellularProfileBuilder(self._request_adapter)

    @property
    def esimcellular_controller(self) -> EsimcellularControllerBuilder:
        """
        The esimcellular-controller property
        """
        from .esimcellular_controller.esimcellular_controller_builder import (
            EsimcellularControllerBuilder,
        )

        return EsimcellularControllerBuilder(self._request_adapter)

    @property
    def esimcellular_profile(self) -> EsimcellularProfileBuilder:
        """
        The esimcellular-profile property
        """
        from .esimcellular_profile.esimcellular_profile_builder import EsimcellularProfileBuilder

        return EsimcellularProfileBuilder(self._request_adapter)

    @property
    def gps(self) -> GpsBuilder:
        """
        The gps property
        """
        from .gps.gps_builder import GpsBuilder

        return GpsBuilder(self._request_adapter)

    @property
    def ipv6_tracker(self) -> Ipv6TrackerBuilder:
        """
        The ipv6-tracker property
        """
        from .ipv6_tracker.ipv6_tracker_builder import Ipv6TrackerBuilder

        return Ipv6TrackerBuilder(self._request_adapter)

    @property
    def ipv6_trackergroup(self) -> Ipv6TrackergroupBuilder:
        """
        The ipv6-trackergroup property
        """
        from .ipv6_trackergroup.ipv6_trackergroup_builder import Ipv6TrackergroupBuilder

        return Ipv6TrackergroupBuilder(self._request_adapter)

    @property
    def management(self) -> ManagementBuilder:
        """
        The management property
        """
        from .management.management_builder import ManagementBuilder

        return ManagementBuilder(self._request_adapter)

    @property
    def routing(self) -> RoutingBuilder:
        """
        The routing property
        """
        from .routing.routing_builder import RoutingBuilder

        return RoutingBuilder(self._request_adapter)

    @property
    def t1_e1_controller(self) -> T1E1ControllerBuilder:
        """
        The t1-e1-controller property
        """
        from .t1_e1_controller.t1_e1_controller_builder import T1E1ControllerBuilder

        return T1E1ControllerBuilder(self._request_adapter)

    @property
    def tracker(self) -> TrackerBuilder:
        """
        The tracker property
        """
        from .tracker.tracker_builder import TrackerBuilder

        return TrackerBuilder(self._request_adapter)

    @property
    def trackergroup(self) -> TrackergroupBuilder:
        """
        The trackergroup property
        """
        from .trackergroup.trackergroup_builder import TrackergroupBuilder

        return TrackergroupBuilder(self._request_adapter)

    @property
    def wan(self) -> WanBuilder:
        """
        The wan property
        """
        from .wan.wan_builder import WanBuilder

        return WanBuilder(self._request_adapter)
