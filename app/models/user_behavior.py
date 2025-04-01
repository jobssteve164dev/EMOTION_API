from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class BehaviorType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CHAT = "chat"
    VIEW_CONTENT = "view_content"
    SEARCH = "search"
    CLICK = "click"
    SCROLL = "scroll"
    SHARE = "share"
    COMMENT = "comment"
    LIKE = "like"
    DISLIKE = "dislike"
    SAVE = "save"
    DELETE = "delete"

class UserBehavior(BaseModel):
    user_id: str
    behavior_type: BehaviorType
    timestamp: datetime
    duration: Optional[float] = None  # 行为持续时间（秒）
    context: Dict  # 行为发生的上下文
    metadata: Optional[Dict] = None  # 额外元数据

class BehaviorPattern(BaseModel):
    daily_pattern: Dict[str, int]  # 每日行为频率
    weekly_pattern: Dict[str, int]  # 每周行为频率
    behavior_sequence: List[Dict[str, float]]  # 行为序列模式
    interaction_graph: Dict[str, Dict[str, float]]  # 行为交互图
    last_updated: datetime

class BehaviorInsight(BaseModel):
    active_hours: List[int]  # 活跃时间段
    favorite_features: List[str]  # 最常用功能
    behavior_clusters: List[Dict[str, float]]  # 行为聚类
    engagement_score: float  # 参与度得分
    retention_score: float  # 留存率得分
    last_updated: datetime

class UserBehaviorProfile(BaseModel):
    user_id: str
    behavior_pattern: BehaviorPattern
    behavior_insight: BehaviorInsight
    behavior_history: List[UserBehavior]
    last_updated: datetime 