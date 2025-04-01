from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.models.user_profile import (
    UserEmotionRecord, UserProfile, EmotionPrediction,
    PersonalizedRecommendation
)
from app.services.user_profile_service import UserProfileService
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()
profile_service = UserProfileService()

@router.post("/emotion-record", response_model=UserProfile)
async def record_emotion(
    emotion_record: UserEmotionRecord,
    current_user: User = Depends(get_current_user)
):
    """
    记录用户情绪数据
    """
    try:
        profile = await profile_service.update_user_profile(
            current_user.id,
            emotion_record
        )
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    获取用户画像
    """
    try:
        profile = await profile_service._get_user_profile(current_user.id)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-emotion", response_model=EmotionPrediction)
async def predict_emotion(
    context: Dict,
    current_user: User = Depends(get_current_user)
):
    """
    预测用户当前情绪
    """
    try:
        prediction = await profile_service.predict_emotion(
            current_user.id,
            context
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations", response_model=List[PersonalizedRecommendation])
async def get_recommendations(
    context: Dict,
    current_user: User = Depends(get_current_user)
):
    """
    获取个性化推荐
    """
    try:
        recommendations = await profile_service.generate_recommendations(
            current_user.id,
            context
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/emotion-stability", response_model=float)
async def get_emotional_stability(
    current_user: User = Depends(get_current_user)
):
    """
    获取情绪稳定性指标
    """
    try:
        profile = await profile_service._get_user_profile(current_user.id)
        return profile.emotional_stability
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 