from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.models.user_behavior import (
    UserBehavior, BehaviorPattern, BehaviorInsight,
    UserBehaviorProfile
)
from app.services.user_behavior_service import UserBehaviorService
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()
behavior_service = UserBehaviorService()

@router.post("/record", response_model=UserBehaviorProfile)
async def record_behavior(
    behavior: UserBehavior,
    current_user: User = Depends(get_current_user)
):
    """
    记录用户行为
    """
    try:
        # 确保行为记录属于当前用户
        behavior.user_id = current_user.id
        
        profile = await behavior_service.record_behavior(behavior)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights", response_model=BehaviorInsight)
async def get_behavior_insights(
    current_user: User = Depends(get_current_user)
):
    """
    获取用户行为洞察
    """
    try:
        insights = await behavior_service.get_behavior_insights(current_user.id)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patterns", response_model=BehaviorPattern)
async def get_behavior_patterns(
    current_user: User = Depends(get_current_user)
):
    """
    获取用户行为模式
    """
    try:
        patterns = await behavior_service.get_behavior_patterns(current_user.id)
        return patterns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile", response_model=UserBehaviorProfile)
async def get_behavior_profile(
    current_user: User = Depends(get_current_user)
):
    """
    获取完整的用户行为画像
    """
    try:
        profile = await behavior_service._get_user_behavior_profile(current_user.id)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 