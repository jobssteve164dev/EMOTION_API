from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class EmotionType(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    ANXIOUS = "anxious"
    CALM = "calm"
    EXCITED = "excited"
    TIRED = "tired"
    FOCUSED = "focused"
    CONFUSED = "confused"
    NEUTRAL = "neutral"

class UserEmotionRecord(BaseModel):
    timestamp: datetime
    emotion_type: EmotionType
    intensity: float  # 0-1
    context: str  # 触发情绪的场景
    source: str  # 数据来源（聊天/反馈/系统分析等）
    text: Optional[str] = None  # 相关文本内容
    metadata: Optional[Dict] = None  # 额外元数据

class UserPersonality(BaseModel):
    openness: float  # 开放性
    conscientiousness: float  # 尽责性
    extraversion: float  # 外向性
    agreeableness: float  # 宜人性
    neuroticism: float  # 神经质
    last_updated: datetime

class UserInterests(BaseModel):
    topics: List[str]  # 感兴趣的话题
    activities: List[str]  # 喜欢的活动
    preferences: Dict[str, float]  # 偏好程度
    last_updated: datetime

class UserEmotionPattern(BaseModel):
    daily_pattern: Dict[str, float]  # 每日情绪变化模式
    weekly_pattern: Dict[str, float]  # 每周情绪变化模式
    triggers: Dict[str, float]  # 情绪触发因素
    coping_strategies: Dict[str, float]  # 应对策略效果
    last_updated: datetime

class UserProfile(BaseModel):
    user_id: str
    personality: UserPersonality
    interests: UserInterests
    emotion_pattern: UserEmotionPattern
    emotion_history: List[UserEmotionRecord]
    current_emotion: Optional[UserEmotionRecord] = None
    emotional_stability: float  # 情绪稳定性指标
    social_profile: Optional[Dict] = None  # 社交情绪数据
    risk_profile: Optional[Dict] = None  # 风险画像数据
    behavior_profile: Optional[Dict] = None  # 行为画像数据
    last_updated: datetime

class EmotionPrediction(BaseModel):
    predicted_emotion: EmotionType
    confidence: float
    factors: Dict[str, float]  # 影响因素
    timestamp: datetime

class PersonalizedRecommendation(BaseModel):
    type: str  # 推荐类型
    content: str  # 推荐内容
    reason: str  # 推荐原因
    relevance_score: float  # 相关度分数
    user_context: Dict  # 用户上下文 