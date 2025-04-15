# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CreatePacketCaptureReq, FormPacketCaptureRes, PacketCaptureInfo

if TYPE_CHECKING:
    from .disable.disable_builder import DisableBuilder
    from .download.download_builder import DownloadBuilder
    from .forcedisbale.forcedisbale_builder import ForcedisbaleBuilder
    from .start.start_builder import StartBuilder
    from .status.status_builder import StatusBuilder
    from .stop.stop_builder import StopBuilder
    from .vnics_info.vnics_info_builder import VnicsInfoBuilder


class CaptureBuilder:
    """
    Builds and executes requests for operations under /stream/device/capture
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def post(self, *, device_uuid: str, session_id: str, **kw) -> FormPacketCaptureRes:
        """
        Form post packet capture
        POST /dataservice/stream/device/capture/{deviceUUID}/{sessionId}

        :param device_uuid: Device uuid
        :param session_id: Session id
        :returns: FormPacketCaptureRes
        """
        ...

    @overload
    def post(self, *, payload: CreatePacketCaptureReq, **kw) -> PacketCaptureInfo:
        """
        Create packet capture session
        POST /dataservice/stream/device/capture

        :param payload: Packet Capture Parameters
        :returns: PacketCaptureInfo
        """
        ...

    def post(
        self,
        *,
        payload: Optional[CreatePacketCaptureReq] = None,
        device_uuid: Optional[str] = None,
        session_id: Optional[str] = None,
        **kw,
    ) -> Union[PacketCaptureInfo, FormPacketCaptureRes]:
        # /dataservice/stream/device/capture/{deviceUUID}/{sessionId}
        if self._request_adapter.param_checker([(device_uuid, str), (session_id, str)], [payload]):
            params = {
                "deviceUUID": device_uuid,
                "sessionId": session_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/stream/device/capture/{deviceUUID}/{sessionId}",
                return_type=FormPacketCaptureRes,
                params=params,
                **kw,
            )
        # /dataservice/stream/device/capture
        if self._request_adapter.param_checker(
            [(payload, CreatePacketCaptureReq)], [device_uuid, session_id]
        ):
            return self._request_adapter.request(
                "POST",
                "/dataservice/stream/device/capture",
                return_type=PacketCaptureInfo,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def disable(self) -> DisableBuilder:
        """
        The disable property
        """
        from .disable.disable_builder import DisableBuilder

        return DisableBuilder(self._request_adapter)

    @property
    def download(self) -> DownloadBuilder:
        """
        The download property
        """
        from .download.download_builder import DownloadBuilder

        return DownloadBuilder(self._request_adapter)

    @property
    def forcedisbale(self) -> ForcedisbaleBuilder:
        """
        The forcedisbale property
        """
        from .forcedisbale.forcedisbale_builder import ForcedisbaleBuilder

        return ForcedisbaleBuilder(self._request_adapter)

    @property
    def start(self) -> StartBuilder:
        """
        The start property
        """
        from .start.start_builder import StartBuilder

        return StartBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def stop(self) -> StopBuilder:
        """
        The stop property
        """
        from .stop.stop_builder import StopBuilder

        return StopBuilder(self._request_adapter)

    @property
    def vnics_info(self) -> VnicsInfoBuilder:
        """
        The vnicsInfo property
        """
        from .vnics_info.vnics_info_builder import VnicsInfoBuilder

        return VnicsInfoBuilder(self._request_adapter)
