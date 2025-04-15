# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanSecurityFeaturePostRequest1,
    CreateSdwanSecurityFeaturePostRequest2,
    CreateSdwanSecurityFeaturePostRequest3,
    CreateSdwanSecurityFeaturePostRequest4,
    CreateSdwanSecurityFeaturePostRequest5,
    CreateSdwanSecurityFeaturePostRequest61,
    CreateSdwanSecurityFeaturePostRequest62,
    CreateSdwanSecurityFeaturePostResponse,
    EditSdwanSecurityFeature1PutRequest1,
    EditSdwanSecurityFeature1PutRequest2,
    EditSdwanSecurityFeature1PutRequest3,
    EditSdwanSecurityFeature1PutRequest4,
    EditSdwanSecurityFeature1PutRequest5,
    EditSdwanSecurityFeature1PutRequest61,
    EditSdwanSecurityFeature1PutRequest62,
    EditSdwanSecurityFeature1PutResponse,
    GetListSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload,
    GetSingleSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload,
    SecurityProfileParcelTypeParam,
)

if TYPE_CHECKING:
    from .advanced_inspection_profile.advanced_inspection_profile_builder import (
        AdvancedInspectionProfileBuilder,
    )
    from .advanced_malware_protection.advanced_malware_protection_builder import (
        AdvancedMalwareProtectionBuilder,
    )
    from .intrusion_prevention.intrusion_prevention_builder import IntrusionPreventionBuilder
    from .ssl_decryption.ssl_decryption_builder import SslDecryptionBuilder
    from .ssl_decryption_profile.ssl_decryption_profile_builder import SslDecryptionProfileBuilder
    from .url_filtering.url_filtering_builder import UrlFilteringBuilder


class UnifiedBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        policy_object_id: str,
        security_profile_parcel_type: SecurityProfileParcelTypeParam,
        payload: Union[
            CreateSdwanSecurityFeaturePostRequest1,
            CreateSdwanSecurityFeaturePostRequest2,
            CreateSdwanSecurityFeaturePostRequest3,
            CreateSdwanSecurityFeaturePostRequest4,
            CreateSdwanSecurityFeaturePostRequest5,
            Union[CreateSdwanSecurityFeaturePostRequest61, CreateSdwanSecurityFeaturePostRequest62],
        ],
        **kw,
    ) -> CreateSdwanSecurityFeaturePostResponse:
        """
        Create Feature for Security Policy
        POST /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}

        :param policy_object_id: Feature Profile ID
        :param security_profile_parcel_type: Policy Object ListType
        :param payload: Security Feature
        :returns: CreateSdwanSecurityFeaturePostResponse
        """
        params = {
            "policyObjectId": policy_object_id,
            "securityProfileParcelType": security_profile_parcel_type,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}",
            return_type=CreateSdwanSecurityFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        policy_object_id: str,
        security_profile_parcel_type: SecurityProfileParcelTypeParam,
        security_profile_parcel_id: str,
        payload: Union[
            EditSdwanSecurityFeature1PutRequest1,
            EditSdwanSecurityFeature1PutRequest2,
            EditSdwanSecurityFeature1PutRequest3,
            EditSdwanSecurityFeature1PutRequest4,
            EditSdwanSecurityFeature1PutRequest5,
            Union[EditSdwanSecurityFeature1PutRequest61, EditSdwanSecurityFeature1PutRequest62],
        ],
        **kw,
    ) -> EditSdwanSecurityFeature1PutResponse:
        """
        Update a Security Feature
        PUT /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}/{securityProfileParcelId}

        :param policy_object_id: Feature Profile ID
        :param security_profile_parcel_type: Policy Object ListType
        :param security_profile_parcel_id: Feature ID
        :param payload: Security Feature
        :returns: EditSdwanSecurityFeature1PutResponse
        """
        params = {
            "policyObjectId": policy_object_id,
            "securityProfileParcelType": security_profile_parcel_type,
            "securityProfileParcelId": security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}/{securityProfileParcelId}",
            return_type=EditSdwanSecurityFeature1PutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self,
        policy_object_id: str,
        security_profile_parcel_type: SecurityProfileParcelTypeParam,
        security_profile_parcel_id: str,
        **kw,
    ):
        """
        Delete a Security Feature
        DELETE /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}/{securityProfileParcelId}

        :param policy_object_id: Feature Profile ID
        :param security_profile_parcel_type: Policy Object ListType
        :param security_profile_parcel_id: Feature ID
        :returns: None
        """
        params = {
            "policyObjectId": policy_object_id,
            "securityProfileParcelType": security_profile_parcel_type,
            "securityProfileParcelId": security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}/{securityProfileParcelId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self,
        *,
        policy_object_id: str,
        security_profile_parcel_type: SecurityProfileParcelTypeParam,
        security_profile_parcel_id: str,
        references: Optional[bool] = False,
        **kw,
    ) -> GetSingleSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload:
        """
        Get Security Feature by FeatureId
        GET /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}/{securityProfileParcelId}

        :param policy_object_id: Feature Profile ID
        :param security_profile_parcel_type: Policy Object ListType
        :param security_profile_parcel_id: Feature ID
        :param references: get associated profile/parcel details
        :returns: GetSingleSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload
        """
        ...

    @overload
    def get(
        self,
        *,
        policy_object_id: str,
        security_profile_parcel_type: SecurityProfileParcelTypeParam,
        reference_count: Optional[bool] = False,
        **kw,
    ) -> GetListSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload:
        """
        Get Security Features for a given ParcelType
        GET /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}

        :param policy_object_id: Feature Profile ID
        :param security_profile_parcel_type: Policy Object ListType
        :param reference_count: get reference count
        :returns: GetListSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload
        """
        ...

    def get(
        self,
        *,
        policy_object_id: str,
        security_profile_parcel_type: SecurityProfileParcelTypeParam,
        reference_count: Optional[bool] = None,
        security_profile_parcel_id: Optional[str] = None,
        references: Optional[bool] = None,
        **kw,
    ) -> Union[
        GetListSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload,
        GetSingleSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}/{securityProfileParcelId}
        if self._request_adapter.param_checker(
            [
                (policy_object_id, str),
                (security_profile_parcel_type, SecurityProfileParcelTypeParam),
                (security_profile_parcel_id, str),
            ],
            [reference_count],
        ):
            params = {
                "policyObjectId": policy_object_id,
                "securityProfileParcelType": security_profile_parcel_type,
                "securityProfileParcelId": security_profile_parcel_id,
                "references": references,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}/{securityProfileParcelId}",
                return_type=GetSingleSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}
        if self._request_adapter.param_checker(
            [
                (policy_object_id, str),
                (security_profile_parcel_type, SecurityProfileParcelTypeParam),
            ],
            [security_profile_parcel_id, references],
        ):
            params = {
                "policyObjectId": policy_object_id,
                "securityProfileParcelType": security_profile_parcel_type,
                "referenceCount": reference_count,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/{securityProfileParcelType}",
                return_type=GetListSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def advanced_inspection_profile(self) -> AdvancedInspectionProfileBuilder:
        """
        The advanced-inspection-profile property
        """
        from .advanced_inspection_profile.advanced_inspection_profile_builder import (
            AdvancedInspectionProfileBuilder,
        )

        return AdvancedInspectionProfileBuilder(self._request_adapter)

    @property
    def advanced_malware_protection(self) -> AdvancedMalwareProtectionBuilder:
        """
        The advanced-malware-protection property
        """
        from .advanced_malware_protection.advanced_malware_protection_builder import (
            AdvancedMalwareProtectionBuilder,
        )

        return AdvancedMalwareProtectionBuilder(self._request_adapter)

    @property
    def intrusion_prevention(self) -> IntrusionPreventionBuilder:
        """
        The intrusion-prevention property
        """
        from .intrusion_prevention.intrusion_prevention_builder import IntrusionPreventionBuilder

        return IntrusionPreventionBuilder(self._request_adapter)

    @property
    def ssl_decryption(self) -> SslDecryptionBuilder:
        """
        The ssl-decryption property
        """
        from .ssl_decryption.ssl_decryption_builder import SslDecryptionBuilder

        return SslDecryptionBuilder(self._request_adapter)

    @property
    def ssl_decryption_profile(self) -> SslDecryptionProfileBuilder:
        """
        The ssl-decryption-profile property
        """
        from .ssl_decryption_profile.ssl_decryption_profile_builder import (
            SslDecryptionProfileBuilder,
        )

        return SslDecryptionProfileBuilder(self._request_adapter)

    @property
    def url_filtering(self) -> UrlFilteringBuilder:
        """
        The url-filtering property
        """
        from .url_filtering.url_filtering_builder import UrlFilteringBuilder

        return UrlFilteringBuilder(self._request_adapter)
