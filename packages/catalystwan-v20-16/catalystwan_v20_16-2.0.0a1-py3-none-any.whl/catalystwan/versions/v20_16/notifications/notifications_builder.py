# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .rule.rule_builder import RuleBuilder
    from .rules.rules_builder import RulesBuilder


class NotificationsBuilder:
    """
    Builds and executes requests for operations under /notifications
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def rule(self) -> RuleBuilder:
        """
        The rule property
        """
        from .rule.rule_builder import RuleBuilder

        return RuleBuilder(self._request_adapter)

    @property
    def rules(self) -> RulesBuilder:
        """
        The rules property
        """
        from .rules.rules_builder import RulesBuilder

        return RulesBuilder(self._request_adapter)
