# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .analytics.analytics_builder import AnalyticsBuilder
    from .certificate.certificate_builder import CertificateBuilder
    from .cloudx.cloudx_builder import CloudxBuilder
    from .google_map_key.google_map_key_builder import GoogleMapKeyBuilder
    from .maintenance_window.maintenance_window_builder import MaintenanceWindowBuilder
    from .microsoft_telemetry.microsoft_telemetry_builder import MicrosoftTelemetryBuilder
    from .wani.wani_builder import WaniBuilder


class ConfigurationBuilder:
    """
    Builds and executes requests for operations under /settings/configuration
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, type_: str, **kw) -> str:
        """
        Retrieve configuration value by type
        GET /dataservice/settings/configuration/{type}

        :param type_: Type of the certificate configuration
        :returns: str
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/settings/configuration/{type}",
            return_type=str,
            params=params,
            **kw,
        )

    def put(self, type_: str, payload: Any, **kw) -> str:
        """
        Update configuration setting
        PUT /dataservice/settings/configuration/{type}

        :param type_: Type of the certificate configuration
        :param payload: Vmanage configuration setting
        :returns: str
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/settings/configuration/{type}",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )

    def post(self, type_: str, payload: Any, **kw) -> str:
        """
        Add new certificate configuration
        POST /dataservice/settings/configuration/{type}

        :param type_: Type of the certificate configuration
        :param payload: Vmanage configuration setting
        :returns: str
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/settings/configuration/{type}",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )

    @property
    def analytics(self) -> AnalyticsBuilder:
        """
        The analytics property
        """
        from .analytics.analytics_builder import AnalyticsBuilder

        return AnalyticsBuilder(self._request_adapter)

    @property
    def certificate(self) -> CertificateBuilder:
        """
        The certificate property
        """
        from .certificate.certificate_builder import CertificateBuilder

        return CertificateBuilder(self._request_adapter)

    @property
    def cloudx(self) -> CloudxBuilder:
        """
        The cloudx property
        """
        from .cloudx.cloudx_builder import CloudxBuilder

        return CloudxBuilder(self._request_adapter)

    @property
    def google_map_key(self) -> GoogleMapKeyBuilder:
        """
        The googleMapKey property
        """
        from .google_map_key.google_map_key_builder import GoogleMapKeyBuilder

        return GoogleMapKeyBuilder(self._request_adapter)

    @property
    def maintenance_window(self) -> MaintenanceWindowBuilder:
        """
        The maintenanceWindow property
        """
        from .maintenance_window.maintenance_window_builder import MaintenanceWindowBuilder

        return MaintenanceWindowBuilder(self._request_adapter)

    @property
    def microsoft_telemetry(self) -> MicrosoftTelemetryBuilder:
        """
        The microsoftTelemetry property
        """
        from .microsoft_telemetry.microsoft_telemetry_builder import MicrosoftTelemetryBuilder

        return MicrosoftTelemetryBuilder(self._request_adapter)

    @property
    def wani(self) -> WaniBuilder:
        """
        The wani property
        """
        from .wani.wani_builder import WaniBuilder

        return WaniBuilder(self._request_adapter)
