from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class InteractionType(str, Enum):
    CHAT = "chat"
    COMMENT = "comment"
    LIKE = "like"
    SHARE = "share"
    FOLLOW = "follow"
    UNFOLLOW = "unfollow"
    MENTION = "mention"

class SocialEmotionRecord(BaseModel):
    user_id: str
    interaction_type: InteractionType
    target_user_id: Optional[str] = None
    emotion_type: str
    intensity: float
    context: str
    timestamp: datetime = datetime.now()
    metadata: Optional[Dict] = None

class SocialEmotionAnalysis(BaseModel):
    user_id: str
    social_emotion_score: float  # 社交情绪得分 (-1 到 1)
    social_engagement: float  # 社交参与度 (0 到 1)
    social_network_size: int  # 社交网络规模
    interaction_patterns: Dict[str, float]  # 互动模式
    emotional_contagion: float  # 情绪传染度
    last_updated: datetime = datetime.now()

class SocialEmotionTrend(BaseModel):
    user_id: str
    time_period: str  # daily, weekly, monthly
    emotion_scores: List[float]
    engagement_scores: List[float]
    network_growth: List[int]
    interaction_counts: Dict[str, List[int]]
    timestamps: List[datetime]

class SocialEmotionInsight(BaseModel):
    user_id: str
    top_interactions: List[Dict[str, float]]  # 最频繁的互动类型
    emotional_impact: Dict[str, float]  # 不同互动对情绪的影响
    social_support: float  # 社交支持度
    social_stress: float  # 社交压力
    relationship_quality: Dict[str, float]  # 与不同用户的关系质量
    last_updated: datetime = datetime.now() 