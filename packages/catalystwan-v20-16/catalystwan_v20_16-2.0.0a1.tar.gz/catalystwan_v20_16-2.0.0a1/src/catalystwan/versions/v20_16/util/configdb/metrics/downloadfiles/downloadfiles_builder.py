# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class DownloadfilesBuilder:
    """
    Builds and executes requests for operations under /util/configdb/metrics/downloadfiles
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        metric_name: str,
        start_date: str,
        end_date: Optional[str] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        **kw,
    ) -> str:
        """
        By passing in the appropriate metric, date, start and end time, it will return a tar file consisting of all the metric files of the respective metric within the timeframe provided
        GET /dataservice/util/configdb/metrics/downloadfiles

        :param metric_name: Pass the metric name
        :param start_date: Date in yyyy-MM-dd format or any Number format. If a number is passed, that will be the number of minutes. The start/end will be translated as <current date/time – minutes passed> and <current date/time> respectively.
        :param end_date: Date in yyyy-MM-dd format. The end date is given if data from multiple dates needs to be extracted. If single date data needed then endDate can be empty. endDate cannot be a previous date to the startDate.
        :param start: Start Time in HHMMSS format; Time in UTC timezone
        :param end: End Time in HHMMSS format; Time in UTC timezone
        :returns: str
        """
        params = {
            "metricName": metric_name,
            "startDate": start_date,
            "endDate": end_date,
            "start": start,
            "end": end,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/util/configdb/metrics/downloadfiles",
            return_type=str,
            params=params,
            **kw,
        )
