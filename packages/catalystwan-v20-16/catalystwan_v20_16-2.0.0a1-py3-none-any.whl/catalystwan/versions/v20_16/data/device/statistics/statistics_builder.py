# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .alarm.alarm_builder import AlarmBuilder
    from .doccount.doccount_builder import DoccountBuilder
    from .fields.fields_builder import FieldsBuilder


class StatisticsBuilder:
    """
    Builds and executes requests for operations under /data/device/statistics
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(
        self,
        state_data_type: str,
        scroll_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        count: Optional[int] = None,
        time_zone: Optional[str] = None,
        **kw,
    ) -> List[Any]:
        """
        Get device statistics data
        GET /dataservice/data/device/statistics/{state_data_type}

        :param state_data_type: State data type
        :param scroll_id: Scroll Id
        :param start_date: Start date
        :param end_date: End date
        :param count: Count
        :param time_zone: Time zone
        :returns: List[Any]
        """
        ...

    @overload
    def get(self, **kw) -> Any:
        """
        Get statistics types
        GET /dataservice/data/device/statistics

        :returns: Any
        """
        ...

    def get(
        self,
        state_data_type: Optional[str] = None,
        scroll_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        count: Optional[int] = None,
        time_zone: Optional[str] = None,
        **kw,
    ) -> Union[Any, List[Any]]:
        # /dataservice/data/device/statistics/{state_data_type}
        if self._request_adapter.param_checker([(state_data_type, str)], []):
            params = {
                "state_data_type": state_data_type,
                "scrollId": scroll_id,
                "startDate": start_date,
                "endDate": end_date,
                "count": count,
                "timeZone": time_zone,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/data/device/statistics/{state_data_type}",
                return_type=List[Any],
                params=params,
                **kw,
            )
        # /dataservice/data/device/statistics
        if self._request_adapter.param_checker(
            [], [state_data_type, scroll_id, start_date, end_date, count, time_zone]
        ):
            return self._request_adapter.request("GET", "/dataservice/data/device/statistics", **kw)
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def alarm(self) -> AlarmBuilder:
        """
        The alarm property
        """
        from .alarm.alarm_builder import AlarmBuilder

        return AlarmBuilder(self._request_adapter)

    @property
    def doccount(self) -> DoccountBuilder:
        """
        The doccount property
        """
        from .doccount.doccount_builder import DoccountBuilder

        return DoccountBuilder(self._request_adapter)

    @property
    def fields(self) -> FieldsBuilder:
        """
        The fields property
        """
        from .fields.fields_builder import FieldsBuilder

        return FieldsBuilder(self._request_adapter)
