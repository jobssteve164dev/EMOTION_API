from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class AlertLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertRule(BaseModel):
    id: str
    name: str
    description: str
    conditions: Dict[str, float]  # 触发条件
    level: AlertLevel
    enabled: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class Alert(BaseModel):
    id: str
    user_id: str
    rule_id: str
    level: AlertLevel
    message: str
    details: Dict
    created_at: datetime = datetime.now()
    resolved_at: Optional[datetime] = None
    status: str = "active"  # active, resolved, dismissed

class AlertHistory(BaseModel):
    user_id: str
    alerts: List[Alert]
    total_alerts: int
    active_alerts: int
    last_alert_time: Optional[datetime] 