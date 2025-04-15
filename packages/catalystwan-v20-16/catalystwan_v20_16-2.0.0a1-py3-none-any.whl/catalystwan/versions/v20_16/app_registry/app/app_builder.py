# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .category.category_builder import CategoryBuilder
    from .discoveredapps.discoveredapps_builder import DiscoveredappsBuilder
    from .filtermap.filtermap_builder import FiltermapBuilder
    from .kubernetesapps.kubernetesapps_builder import KubernetesappsBuilder


class AppBuilder:
    """
    Builds and executes requests for operations under /app-registry/app
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        filter_attribute_type: Optional[str] = None,
        filter_attribute_value: Optional[str] = None,
        **kw,
    ) -> List[Any]:
        """
        Get All the App for the given conditions
        GET /dataservice/app-registry/app

        :param filter_attribute_type: Filter attribute type
        :param filter_attribute_value: Filter attribute value
        :returns: List[Any]
        """
        params = {
            "filterAttributeType": filter_attribute_type,
            "filterAttributeValue": filter_attribute_value,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/app-registry/app", return_type=List[Any], params=params, **kw
        )

    @property
    def category(self) -> CategoryBuilder:
        """
        The category property
        """
        from .category.category_builder import CategoryBuilder

        return CategoryBuilder(self._request_adapter)

    @property
    def discoveredapps(self) -> DiscoveredappsBuilder:
        """
        The discoveredapps property
        """
        from .discoveredapps.discoveredapps_builder import DiscoveredappsBuilder

        return DiscoveredappsBuilder(self._request_adapter)

    @property
    def filtermap(self) -> FiltermapBuilder:
        """
        The filtermap property
        """
        from .filtermap.filtermap_builder import FiltermapBuilder

        return FiltermapBuilder(self._request_adapter)

    @property
    def kubernetesapps(self) -> KubernetesappsBuilder:
        """
        The kubernetesapps property
        """
        from .kubernetesapps.kubernetesapps_builder import KubernetesappsBuilder

        return KubernetesappsBuilder(self._request_adapter)
