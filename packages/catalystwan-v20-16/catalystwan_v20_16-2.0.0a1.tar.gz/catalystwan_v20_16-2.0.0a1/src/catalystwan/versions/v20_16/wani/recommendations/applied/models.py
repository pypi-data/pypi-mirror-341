# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field


@dataclass
class AppliedRecommendationsResEntry:
    action_id: str = _field(metadata={"alias": "actionId"})
    app_class_name: str = _field(metadata={"alias": "appClassName"})
    last_updated: str = _field(metadata={"alias": "last updated"})
    recommendation_def: str = _field(metadata={"alias": "recommendationDef"})
    site_id: str = _field(metadata={"alias": "siteId"})
    state: str
