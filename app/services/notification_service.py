from typing import List, Dict, Optional
from datetime import datetime
from app.models.alert import Alert, AlertLevel
import aiohttp
import json

class NotificationService:
    def __init__(self):
        self.webhook_urls = {
            AlertLevel.LOW: "http://notification-service/webhook/low",
            AlertLevel.MEDIUM: "http://notification-service/webhook/medium",
            AlertLevel.HIGH: "http://notification-service/webhook/high",
            AlertLevel.CRITICAL: "http://notification-service/webhook/critical"
        }
    
    async def send_alert_notification(self, alert: Alert) -> bool:
        """发送预警通知"""
        try:
            webhook_url = self.webhook_urls.get(alert.level)
            if not webhook_url:
                return False
            
            notification_data = {
                "alert_id": alert.id,
                "user_id": alert.user_id,
                "level": alert.level,
                "message": alert.message,
                "details": alert.details,
                "timestamp": datetime.now().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    webhook_url,
                    json=notification_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            print(f"发送通知失败: {str(e)}")
            return False
    
    async def send_batch_notifications(self, alerts: List[Alert]) -> Dict[str, int]:
        """批量发送预警通知"""
        results = {
            "success": 0,
            "failed": 0
        }
        
        for alert in alerts:
            success = await self.send_alert_notification(alert)
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    async def send_alert_summary(self, user_id: str, alert_history: Dict) -> bool:
        """发送预警汇总报告"""
        try:
            summary_data = {
                "user_id": user_id,
                "total_alerts": alert_history["total_alerts"],
                "active_alerts": alert_history["active_alerts"],
                "last_alert_time": alert_history["last_alert_time"],
                "alert_levels": self._count_alert_levels(alert_history["alerts"]),
                "timestamp": datetime.now().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://notification-service/webhook/summary",
                    json=summary_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            print(f"发送汇总报告失败: {str(e)}")
            return False
    
    def _count_alert_levels(self, alerts: List[Alert]) -> Dict[str, int]:
        """统计各预警级别的数量"""
        counts = {
            AlertLevel.LOW: 0,
            AlertLevel.MEDIUM: 0,
            AlertLevel.HIGH: 0,
            AlertLevel.CRITICAL: 0
        }
        
        for alert in alerts:
            counts[alert.level] += 1
        
        return counts 