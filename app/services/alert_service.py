from datetime import datetime, timedelta
from typing import List, Dict, Optional
from app.models.alert import Alert, AlertRule, AlertLevel, AlertHistory
from app.models.user_profile import UserEmotionRecord
from app.services.user_profile_service import UserProfileService
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class AlertService:
    def __init__(self):
        self.profile_service = UserProfileService()
        self.default_rules = self._create_default_rules()
    
    def _create_default_rules(self) -> List[AlertRule]:
        """创建默认预警规则"""
        return [
            AlertRule(
                id="rule_1",
                name="持续负面情绪",
                description="连续3天出现强烈负面情绪",
                conditions={
                    "negative_intensity_threshold": 0.7,
                    "consecutive_days": 3
                },
                level=AlertLevel.HIGH
            ),
            AlertRule(
                id="rule_2",
                name="情绪波动异常",
                description="24小时内情绪波动超过阈值",
                conditions={
                    "emotion_volatility_threshold": 0.8,
                    "time_window_hours": 24
                },
                level=AlertLevel.MEDIUM
            ),
            AlertRule(
                id="rule_3",
                name="情绪稳定性下降",
                description="情绪稳定性指标显著下降",
                conditions={
                    "stability_drop_threshold": 0.3,
                    "time_window_days": 7
                },
                level=AlertLevel.MEDIUM
            )
        ]
    
    async def check_alerts(self, user_id: str, emotion_record: UserEmotionRecord) -> List[Alert]:
        """检查是否需要触发预警"""
        alerts = []
        profile = await self.profile_service._get_user_profile(user_id)
        
        # 检查每个规则
        for rule in self.default_rules:
            if not rule.enabled:
                continue
                
            alert = await self._evaluate_rule(rule, user_id, emotion_record, profile)
            if alert:
                alerts.append(alert)
        
        return alerts
    
    async def _evaluate_rule(self, rule: AlertRule, user_id: str, 
                           emotion_record: UserEmotionRecord, profile) -> Optional[Alert]:
        """评估单个规则"""
        if rule.id == "rule_1":
            return await self._check_negative_emotion_rule(rule, user_id, emotion_record, profile)
        elif rule.id == "rule_2":
            return await self._check_emotion_volatility_rule(rule, user_id, emotion_record, profile)
        elif rule.id == "rule_3":
            return await self._check_stability_drop_rule(rule, user_id, emotion_record, profile)
        return None
    
    async def _check_negative_emotion_rule(self, rule: AlertRule, user_id: str,
                                         emotion_record: UserEmotionRecord, profile) -> Optional[Alert]:
        """检查持续负面情绪规则"""
        threshold = rule.conditions["negative_intensity_threshold"]
        consecutive_days = rule.conditions["consecutive_days"]
        
        # 获取最近的情绪记录
        recent_records = [r for r in profile.emotion_history 
                         if r.timestamp >= datetime.now() - timedelta(days=consecutive_days)]
        
        if len(recent_records) >= consecutive_days:
            negative_count = sum(1 for r in recent_records 
                               if r.emotion_type in ["sad", "angry", "anxious"] 
                               and r.intensity >= threshold)
            
            if negative_count >= consecutive_days:
                return Alert(
                    id=f"alert_{datetime.now().timestamp()}",
                    user_id=user_id,
                    rule_id=rule.id,
                    level=rule.level,
                    message=f"检测到连续{consecutive_days}天出现强烈负面情绪",
                    details={
                        "negative_count": negative_count,
                        "average_intensity": sum(r.intensity for r in recent_records) / len(recent_records)
                    }
                )
        return None
    
    async def _check_emotion_volatility_rule(self, rule: AlertRule, user_id: str,
                                           emotion_record: UserEmotionRecord, profile) -> Optional[Alert]:
        """检查情绪波动异常规则"""
        threshold = rule.conditions["emotion_volatility_threshold"]
        time_window = timedelta(hours=rule.conditions["time_window_hours"])
        
        # 获取时间窗口内的情绪记录
        window_records = [r for r in profile.emotion_history 
                         if r.timestamp >= datetime.now() - time_window]
        
        if len(window_records) >= 2:
            intensities = [r.intensity for r in window_records]
            volatility = max(intensities) - min(intensities)
            
            if volatility >= threshold:
                return Alert(
                    id=f"alert_{datetime.now().timestamp()}",
                    user_id=user_id,
                    rule_id=rule.id,
                    level=rule.level,
                    message=f"检测到{time_window.total_seconds()/3600}小时内情绪波动异常",
                    details={
                        "volatility": volatility,
                        "max_intensity": max(intensities),
                        "min_intensity": min(intensities)
                    }
                )
        return None
    
    async def _check_stability_drop_rule(self, rule: AlertRule, user_id: str,
                                       emotion_record: UserEmotionRecord, profile) -> Optional[Alert]:
        """检查情绪稳定性下降规则"""
        threshold = rule.conditions["stability_drop_threshold"]
        time_window = timedelta(days=rule.conditions["time_window_days"])
        
        # 计算当前稳定性
        current_stability = profile.emotional_stability
        
        # 获取历史稳定性数据
        historical_stability = await self._get_historical_stability(user_id, time_window)
        
        if historical_stability:
            stability_drop = historical_stability - current_stability
            
            if stability_drop >= threshold:
                return Alert(
                    id=f"alert_{datetime.now().timestamp()}",
                    user_id=user_id,
                    rule_id=rule.id,
                    level=rule.level,
                    message=f"检测到情绪稳定性显著下降",
                    details={
                        "stability_drop": stability_drop,
                        "current_stability": current_stability,
                        "historical_stability": historical_stability
                    }
                )
        return None
    
    async def _get_historical_stability(self, user_id: str, time_window: timedelta) -> Optional[float]:
        """获取历史情绪稳定性数据"""
        # TODO: 实现从数据库获取历史稳定性数据
        return 0.8  # 示例返回值
    
    async def get_alert_history(self, user_id: str) -> AlertHistory:
        """获取用户预警历史"""
        # TODO: 实现从数据库获取预警历史
        return AlertHistory(
            user_id=user_id,
            alerts=[],
            total_alerts=0,
            active_alerts=0,
            last_alert_time=None
        )
    
    async def resolve_alert(self, alert_id: str) -> Alert:
        """解决预警"""
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        
        # 查找预警
        alert_data = await db.alerts.find_one({"id": alert_id})
        
        if not alert_data:
            raise ValueError(f"找不到ID为{alert_id}的预警")
            
        # 更新预警状态为已解决
        alert_data["status"] = "resolved"
        alert_data["resolved_at"] = datetime.now()
        
        # 更新数据库
        await db.alerts.update_one(
            {"id": alert_id},
            {"$set": {"status": "resolved", "resolved_at": datetime.now()}}
        )
        
        # 返回更新后的预警对象
        return Alert(**alert_data)
    
    async def dismiss_alert(self, alert_id: str) -> Alert:
        """忽略预警"""
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        
        # 查找预警
        alert_data = await db.alerts.find_one({"id": alert_id})
        
        if not alert_data:
            raise ValueError(f"找不到ID为{alert_id}的预警")
            
        # 更新预警状态为已忽略
        alert_data["status"] = "dismissed"
        
        # 更新数据库
        await db.alerts.update_one(
            {"id": alert_id},
            {"$set": {"status": "dismissed"}}
        )
        
        # 返回更新后的预警对象
        return Alert(**alert_data) 