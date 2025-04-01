from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EmotionAnalysis(BaseModel):
    text: str
    score: float  # 情感得分 (-1 到 1)
    emotion: str  # 主要情绪
    confidence: float  # 置信度
    timestamp: datetime = datetime.now()

class EmotionHistory(BaseModel):
    user_id: str
    analyses: List[EmotionAnalysis]
    average_score: float
    dominant_emotion: str
    trend: List[float]  # 情绪趋势数据

class EmotionResponse(BaseModel):
    analysis: EmotionAnalysis
    suggestions: List[str]
    trend_data: Optional[List[float]] = None

class UserEmotionProfile(BaseModel):
    user_id: str
    overall_mood: float
    emotional_stability: float
    common_emotions: List[str]
    last_updated: datetime 