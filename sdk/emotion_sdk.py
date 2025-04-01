import requests
from typing import Dict, Optional, List
from datetime import datetime
from app.models.social_emotion import SocialEmotionRecord

class EmotionSDK:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        初始化情感分析SDK
        
        Args:
            base_url: API基础URL
            api_key: API密钥（可选）
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self._token = None

    def login(self, username: str, password: str) -> bool:
        """
        登录获取访问令牌
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            bool: 登录是否成功
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/auth/token",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                self._token = data["access_token"]
                self.session.headers.update({
                    "Authorization": f"Bearer {self._token}"
                })
                return True
            return False
        except Exception as e:
            print(f"登录失败: {str(e)}")
            return False

    def analyze_emotion(self, text: str) -> Dict:
        """
        分析文本情感
        
        Args:
            text: 待分析文本
            
        Returns:
            Dict: 分析结果
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.post(
            f"{self.base_url}/api/v1/emotion/analyze",
            json={"text": text}
        )
        response.raise_for_status()
        return response.json()

    def get_emotion_history(self, user_id: str, start_date: Optional[datetime] = None, 
                          end_date: Optional[datetime] = None) -> List[Dict]:
        """
        获取用户情感历史记录
        
        Args:
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            List[Dict]: 历史记录列表
        """
        if not self._token:
            raise Exception("请先登录")
            
        params = {"user_id": user_id}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
            
        response = self.session.get(
            f"{self.base_url}/api/v1/emotion/history",
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_emotion_trend(self, user_id: str, days: int = 30) -> Dict:
        """
        获取用户情感趋势
        
        Args:
            user_id: 用户ID
            days: 天数
            
        Returns:
            Dict: 趋势数据
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.get(
            f"{self.base_url}/api/v1/emotion/trend",
            params={"user_id": user_id, "days": days}
        )
        response.raise_for_status()
        return response.json()

    def get_alert_rules(self) -> List[Dict]:
        """
        获取预警规则列表
        
        Returns:
            List[Dict]: 预警规则列表
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.get(
            f"{self.base_url}/api/v1/alert/rules"
        )
        response.raise_for_status()
        return response.json()

    def get_alert_history(self) -> Dict:
        """
        获取预警历史
        
        Returns:
            Dict: 预警历史数据
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.get(
            f"{self.base_url}/api/v1/alert/history"
        )
        response.raise_for_status()
        return response.json()

    def resolve_alert(self, alert_id: str) -> Dict:
        """
        解决预警
        
        Args:
            alert_id: 预警ID
            
        Returns:
            Dict: 更新后的预警信息
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.post(
            f"{self.base_url}/api/v1/alert/resolve/{alert_id}"
        )
        response.raise_for_status()
        return response.json()

    def dismiss_alert(self, alert_id: str) -> Dict:
        """
        忽略预警
        
        Args:
            alert_id: 预警ID
            
        Returns:
            Dict: 更新后的预警信息
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.post(
            f"{self.base_url}/api/v1/alert/dismiss/{alert_id}"
        )
        response.raise_for_status()
        return response.json()

    def get_alert_summary(self) -> Dict:
        """
        获取预警汇总报告
        
        Returns:
            Dict: 汇总报告数据
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.get(
            f"{self.base_url}/api/v1/alert/summary"
        )
        response.raise_for_status()
        return response.json()

    def record_social_interaction(self, record: SocialEmotionRecord) -> Dict:
        """
        记录社交互动
        
        Args:
            record: 社交互动记录
            
        Returns:
            Dict: 记录结果
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.post(
            f"{self.base_url}/api/v1/social/interactions",
            json=record.dict()
        )
        response.raise_for_status()
        return response.json()

    def get_social_emotion_analysis(self, user_id: str) -> Dict:
        """
        获取社交情绪分析
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 分析结果
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.get(
            f"{self.base_url}/api/v1/social/analysis/{user_id}"
        )
        response.raise_for_status()
        return response.json()

    def get_social_emotion_trend(self, user_id: str, time_period: str) -> Dict:
        """
        获取社交情绪趋势
        
        Args:
            user_id: 用户ID
            time_period: 时间周期
            
        Returns:
            Dict: 趋势数据
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.get(
            f"{self.base_url}/api/v1/social/trend/{user_id}",
            params={"time_period": time_period}
        )
        response.raise_for_status()
        return response.json()

    def get_social_emotion_insights(self, user_id: str) -> Dict:
        """
        获取社交情绪洞察
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 洞察数据
        """
        if not self._token:
            raise Exception("请先登录")
            
        response = self.session.get(
            f"{self.base_url}/api/v1/social/insights/{user_id}"
        )
        response.raise_for_status()
        return response.json()

    def close(self):
        """关闭会话"""
        self.session.close() 