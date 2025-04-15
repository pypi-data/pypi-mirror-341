# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class NotificationsRuleData:
    _rid: Optional[int] = _field(default=None, metadata={"alias": "@rid"})
    account_details: Optional[str] = _field(default=None, metadata={"alias": "accountDetails"})
    alarm_name: Optional[str] = _field(default=None, metadata={"alias": "alarmName"})
    devices_attached: Optional[str] = _field(default=None, metadata={"alias": "devicesAttached"})
    email_threshold: Optional[int] = _field(default=None, metadata={"alias": "emailThreshold"})
    last_updated: Optional[int] = _field(default=None, metadata={"alias": "lastUpdated"})
    notification_rule_id: Optional[str] = _field(
        default=None, metadata={"alias": "notificationRuleId"}
    )
    notification_rule_name: Optional[str] = _field(
        default=None, metadata={"alias": "notificationRuleName"}
    )
    severity: Optional[str] = _field(default=None)
    updated_by: Optional[str] = _field(default=None, metadata={"alias": "updatedBy"})
    webhook_password: Optional[str] = _field(default=None, metadata={"alias": "webhookPassword"})
    webhook_url: Optional[str] = _field(default=None, metadata={"alias": "webhookUrl"})
    webhook_username: Optional[str] = _field(default=None, metadata={"alias": "webhookUsername"})


@dataclass
class NotificationsRulesResponse:
    data: Optional[List[NotificationsRuleData]] = _field(default=None)
