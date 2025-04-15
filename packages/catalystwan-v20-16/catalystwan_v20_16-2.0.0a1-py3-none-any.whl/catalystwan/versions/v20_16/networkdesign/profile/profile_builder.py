# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .attachment.attachment_builder import AttachmentBuilder
    from .feature.feature_builder import FeatureBuilder
    from .lock.lock_builder import LockBuilder
    from .status.status_builder import StatusBuilder
    from .task.task_builder import TaskBuilder
    from .template.template_builder import TemplateBuilder


class ProfileBuilder:
    """
    Builds and executes requests for operations under /networkdesign/profile
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def attachment(self) -> AttachmentBuilder:
        """
        The attachment property
        """
        from .attachment.attachment_builder import AttachmentBuilder

        return AttachmentBuilder(self._request_adapter)

    @property
    def feature(self) -> FeatureBuilder:
        """
        The feature property
        """
        from .feature.feature_builder import FeatureBuilder

        return FeatureBuilder(self._request_adapter)

    @property
    def lock(self) -> LockBuilder:
        """
        The lock property
        """
        from .lock.lock_builder import LockBuilder

        return LockBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def task(self) -> TaskBuilder:
        """
        The task property
        """
        from .task.task_builder import TaskBuilder

        return TaskBuilder(self._request_adapter)

    @property
    def template(self) -> TemplateBuilder:
        """
        The template property
        """
        from .template.template_builder import TemplateBuilder

        return TemplateBuilder(self._request_adapter)
