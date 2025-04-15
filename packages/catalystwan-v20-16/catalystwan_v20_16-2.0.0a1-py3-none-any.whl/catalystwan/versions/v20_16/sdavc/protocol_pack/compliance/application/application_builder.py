# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, overload

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .initiate_compliance.initiate_compliance_builder import InitiateComplianceBuilder
    from .is_compliance_detected.is_compliance_detected_builder import IsComplianceDetectedBuilder
    from .status.status_builder import StatusBuilder


class ApplicationBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance/application
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, uuid: str, **kw) -> Any:
        """
        Get application name compliance details for given task uuid
        GET /dataservice/sdavc/protocol-pack/compliance/application/{uuid}

        :param uuid: Uuid
        :returns: Any
        """
        ...

    @overload
    def get(self, **kw) -> Any:
        """
        Get default application name compliance details
        GET /dataservice/sdavc/protocol-pack/compliance/application

        :returns: Any
        """
        ...

    def get(self, uuid: Optional[str] = None, **kw) -> Any:
        # /dataservice/sdavc/protocol-pack/compliance/application/{uuid}
        if self._request_adapter.param_checker([(uuid, str)], []):
            params = {
                "uuid": uuid,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/sdavc/protocol-pack/compliance/application/{uuid}",
                params=params,
                **kw,
            )
        # /dataservice/sdavc/protocol-pack/compliance/application
        if self._request_adapter.param_checker([], [uuid]):
            return self._request_adapter.request(
                "GET", "/dataservice/sdavc/protocol-pack/compliance/application", **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def initiate_compliance(self) -> InitiateComplianceBuilder:
        """
        The initiate-compliance property
        """
        from .initiate_compliance.initiate_compliance_builder import InitiateComplianceBuilder

        return InitiateComplianceBuilder(self._request_adapter)

    @property
    def is_compliance_detected(self) -> IsComplianceDetectedBuilder:
        """
        The is-compliance-detected property
        """
        from .is_compliance_detected.is_compliance_detected_builder import (
            IsComplianceDetectedBuilder,
        )

        return IsComplianceDetectedBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
