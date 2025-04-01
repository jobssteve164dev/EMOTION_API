from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional
from app.models.user_profile import (
    UserEmotionRecord, UserProfile, EmotionPrediction,
    PersonalizedRecommendation
)
from app.services.user_profile_service import UserProfileService
from app.services.social_emotion_service import SocialEmotionService
from app.services.alert_service import AlertService
from app.services.user_behavior_service import UserBehaviorService
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()
user_profile_service = UserProfileService()
social_emotion_service = SocialEmotionService()
alert_service = AlertService()
user_behavior_service = UserBehaviorService()

@router.post("/emotion-record", response_model=UserProfile)
async def record_emotion(
    emotion_record: UserEmotionRecord,
    current_user: User = Depends(get_current_user)
):
    """
    记录用户情绪数据
    """
    try:
        profile = await user_profile_service.update_user_profile(
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
        profile = await user_profile_service._get_user_profile(current_user.id)
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
        prediction = await user_profile_service.predict_emotion(
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
        recommendations = await user_profile_service.generate_recommendations(
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
        profile = await user_profile_service._get_user_profile(current_user.id)
        return profile.emotional_stability
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comprehensive/{user_id}")
async def get_comprehensive_user_profile(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    获取综合用户画像，包含所有功能的数据整合
    """
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权查看其他用户的画像")
        
    # 获取基础用户画像
    profile = await user_profile_service._get_user_profile(user_id)
    
    # 获取社交情绪数据
    social_emotion_analysis = await social_emotion_service.analyze_social_emotion(user_id)
    social_emotion_insights = await social_emotion_service.get_social_emotion_insights(user_id)
    
    # 获取风险预警数据
    alerts = await alert_service.get_user_alerts(user_id)
    risk_level = await alert_service.calculate_user_risk_level(user_id)
    
    # 获取行为分析数据
    behavior_insights = await user_behavior_service.get_behavior_insights(user_id)
    behavior_patterns = await user_behavior_service.get_behavior_patterns(user_id)
    
    # 整合到用户画像
    profile.social_profile = {
        "social_emotion_score": social_emotion_analysis.social_emotion_score,
        "social_engagement": social_emotion_analysis.social_engagement,
        "social_network_size": social_emotion_analysis.social_network_size,
        "interaction_patterns": social_emotion_analysis.interaction_patterns,
        "emotional_contagion": social_emotion_analysis.emotional_contagion,
        "social_support": social_emotion_insights.social_support,
        "social_stress": social_emotion_insights.social_stress,
        "relationship_quality": social_emotion_insights.relationship_quality
    }
    
    profile.risk_profile = {
        "alert_level": risk_level,
        "active_alerts": len([a for a in alerts if a.status == "active"]),
        "risk_factors": [
            {
                "type": alert.rule_id,
                "level": alert.level,
                "description": alert.message
            }
            for alert in alerts if alert.status == "active"
        ],
        "protective_factors": [
            {
                "type": "strong_social_support" if profile.social_profile["social_support"] > 0.7 else "moderate_social_support",
                "level": "high" if profile.social_profile["social_support"] > 0.7 else "medium",
                "description": "有良好的社交支持网络" if profile.social_profile["social_support"] > 0.7 else "有一定的社交支持网络"
            }
        ]
    }
    
    profile.behavior_profile = {
        "active_hours": behavior_patterns.active_hours,
        "preferred_activities": behavior_patterns.preferred_activities,
        "interaction_patterns": behavior_patterns.interaction_patterns
    }
    
    # 生成推荐
    context = {
        "social_score": profile.social_profile["social_emotion_score"],
        "risk_level": profile.risk_profile["alert_level"],
        "active_hours": profile.behavior_profile["active_hours"]
    }
    recommendations = await user_profile_service.generate_recommendations(user_id, context)
    
    # 构建完整响应
    response = {
        "user_id": profile.user_id,
        "basic_info": {
            "age": 28,  # 假设数据
            "gender": "male",  # 假设数据
            "occupation": "软件工程师",  # 假设数据
            "location": "北京"  # 假设数据
        },
        "emotional_profile": {
            "current_emotion": profile.current_emotion.emotion_type if profile.current_emotion else "neutral",
            "emotion_stability": profile.emotional_stability,
            "dominant_emotions": profile.emotion_pattern.triggers,
            "emotion_trend": profile.emotion_pattern.daily_pattern
        },
        "social_profile": profile.social_profile,
        "behavior_profile": profile.behavior_profile,
        "risk_profile": profile.risk_profile,
        "recommendations": {
            "emotional_health": [r.content for r in recommendations if r.type == "emotional"],
            "social_health": [r.content for r in recommendations if r.type == "social"],
            "behavior_improvement": [r.content for r in recommendations if r.type == "behavior"],
            "risk_prevention": [r.content for r in recommendations if r.type == "risk"]
        },
        "last_updated": profile.last_updated
    }
    
    return response 