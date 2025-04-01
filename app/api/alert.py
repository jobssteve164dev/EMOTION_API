from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.models.alert import Alert, AlertRule, AlertHistory
from app.services.alert_service import AlertService
from app.services.notification_service import NotificationService
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter()
alert_service = AlertService()
notification_service = NotificationService()

@router.get("/rules", response_model=List[AlertRule])
async def get_alert_rules(current_user: User = Depends(get_current_user)):
    """获取预警规则列表"""
    return alert_service.default_rules

@router.get("/history", response_model=AlertHistory)
async def get_alert_history(current_user: User = Depends(get_current_user)):
    """获取预警历史"""
    return await alert_service.get_alert_history(current_user.id)

@router.post("/resolve/{alert_id}", response_model=Alert)
async def resolve_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user)
):
    """解决预警"""
    try:
        alert = await alert_service.resolve_alert(alert_id)
        if alert.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="无权操作此预警")
        return alert
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dismiss/{alert_id}", response_model=Alert)
async def dismiss_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user)
):
    """忽略预警"""
    try:
        alert = await alert_service.dismiss_alert(alert_id)
        if alert.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="无权操作此预警")
        return alert
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_alert_summary(current_user: User = Depends(get_current_user)):
    """获取预警汇总报告"""
    try:
        alert_history = await alert_service.get_alert_history(current_user.id)
        success = await notification_service.send_alert_summary(
            current_user.id,
            alert_history.dict()
        )
        if not success:
            raise HTTPException(status_code=500, detail="生成汇总报告失败")
        return {"status": "success", "message": "汇总报告已发送"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 