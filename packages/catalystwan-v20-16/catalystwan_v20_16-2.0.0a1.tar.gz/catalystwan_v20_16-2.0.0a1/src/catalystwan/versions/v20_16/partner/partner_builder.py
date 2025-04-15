# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    PartnerRes,
    RegisterPartnerRequest,
    RegisterPartnerRes,
    StatusResponse,
    UpdatePartnerRequest,
)

if TYPE_CHECKING:
    from .aci.aci_builder import AciBuilder
    from .dnac.dnac_builder import DnacBuilder
    from .map.map_builder import MapBuilder
    from .unmap.unmap_builder import UnmapBuilder
    from .vpn.vpn_builder import VpnBuilder
    from .wcm.wcm_builder import WcmBuilder


class PartnerBuilder:
    """
    Builds and executes requests for operations under /partner
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, partner_type: str, payload: RegisterPartnerRequest, **kw) -> RegisterPartnerRes:
        """
        Register NMS partner
        POST /dataservice/partner/{partnerType}

        :param partner_type: Partner type
        :param payload: Partner
        :returns: RegisterPartnerRes
        """
        params = {
            "partnerType": partner_type,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/partner/{partnerType}",
            return_type=RegisterPartnerRes,
            params=params,
            payload=payload,
            **kw,
        )

    def put(self, partner_type: str, nms_id: str, payload: UpdatePartnerRequest, **kw):
        """
        Update NMS partner details
        PUT /dataservice/partner/{partnerType}/{nmsId}

        :param partner_type: Partner type
        :param nms_id: Nms id
        :param payload: Partner
        :returns: None
        """
        params = {
            "partnerType": partner_type,
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/partner/{partnerType}/{nmsId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, partner_type: str, nms_id: str, **kw) -> StatusResponse:
        """
        Delete NMS partner
        DELETE /dataservice/partner/{partnerType}/{nmsId}

        :param partner_type: Partner type
        :param nms_id: Nms id
        :returns: StatusResponse
        """
        params = {
            "partnerType": partner_type,
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/partner/{partnerType}/{nmsId}",
            return_type=StatusResponse,
            params=params,
            **kw,
        )

    @overload
    def get(self, partner_type: str, nms_id: str, **kw) -> PartnerRes:
        """
        Get NMS partners by partner type and Id
        GET /dataservice/partner/{partnerType}/{nmsId}

        :param partner_type: Partner type
        :param nms_id: Nms id
        :returns: PartnerRes
        """
        ...

    @overload
    def get(self, partner_type: str, **kw) -> List[PartnerRes]:
        """
        Get NMS partners by partner type
        GET /dataservice/partner/{partnerType}

        :param partner_type: Partner type
        :returns: List[PartnerRes]
        """
        ...

    @overload
    def get(self, **kw) -> List[PartnerRes]:
        """
        Get all NMS partners
        GET /dataservice/partner

        :returns: List[PartnerRes]
        """
        ...

    def get(
        self, partner_type: Optional[str] = None, nms_id: Optional[str] = None, **kw
    ) -> Union[List[PartnerRes], PartnerRes]:
        # /dataservice/partner/{partnerType}/{nmsId}
        if self._request_adapter.param_checker([(partner_type, str), (nms_id, str)], []):
            params = {
                "partnerType": partner_type,
                "nmsId": nms_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/partner/{partnerType}/{nmsId}",
                return_type=PartnerRes,
                params=params,
                **kw,
            )
        # /dataservice/partner/{partnerType}
        if self._request_adapter.param_checker([(partner_type, str)], [nms_id]):
            params = {
                "partnerType": partner_type,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/partner/{partnerType}",
                return_type=List[PartnerRes],
                params=params,
                **kw,
            )
        # /dataservice/partner
        if self._request_adapter.param_checker([], [partner_type, nms_id]):
            return self._request_adapter.request(
                "GET", "/dataservice/partner", return_type=List[PartnerRes], **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def aci(self) -> AciBuilder:
        """
        The aci property
        """
        from .aci.aci_builder import AciBuilder

        return AciBuilder(self._request_adapter)

    @property
    def dnac(self) -> DnacBuilder:
        """
        The dnac property
        """
        from .dnac.dnac_builder import DnacBuilder

        return DnacBuilder(self._request_adapter)

    @property
    def map(self) -> MapBuilder:
        """
        The map property
        """
        from .map.map_builder import MapBuilder

        return MapBuilder(self._request_adapter)

    @property
    def unmap(self) -> UnmapBuilder:
        """
        The unmap property
        """
        from .unmap.unmap_builder import UnmapBuilder

        return UnmapBuilder(self._request_adapter)

    @property
    def vpn(self) -> VpnBuilder:
        """
        The vpn property
        """
        from .vpn.vpn_builder import VpnBuilder

        return VpnBuilder(self._request_adapter)

    @property
    def wcm(self) -> WcmBuilder:
        """
        The wcm property
        """
        from .wcm.wcm_builder import WcmBuilder

        return WcmBuilder(self._request_adapter)
