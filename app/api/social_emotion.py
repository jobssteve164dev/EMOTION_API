from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.models.social_emotion import (
    SocialEmotionRecord, SocialEmotionAnalysis,
    SocialEmotionTrend, SocialEmotionInsight
)
from app.services.social_emotion_service import SocialEmotionService
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()
social_emotion_service = SocialEmotionService()

@router.post("/interactions", response_model=SocialEmotionRecord)
async def record_interaction(
    record: SocialEmotionRecord,
    current_user: User = Depends(get_current_user)
):
    """
    记录社交互动
    """
    if record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权记录其他用户的互动")
    return await social_emotion_service.record_social_interaction(record)

@router.get("/analysis/{user_id}", response_model=SocialEmotionAnalysis)
async def get_social_emotion_analysis(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    获取社交情绪分析
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看其他用户的分析")
    return await social_emotion_service.analyze_social_emotion(user_id)

@router.get("/trend/{user_id}", response_model=SocialEmotionTrend)
async def get_social_emotion_trend(
    user_id: str,
    time_period: str,
    current_user: User = Depends(get_current_user)
):
    """
    获取社交情绪趋势
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看其他用户的趋势")
    return await social_emotion_service.get_social_emotion_trend(user_id, time_period)

@router.get("/insights/{user_id}", response_model=SocialEmotionInsight)
async def get_social_emotion_insights(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    获取社交情绪洞察
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看其他用户的洞察")
    return await social_emotion_service.get_social_emotion_insights(user_id) 