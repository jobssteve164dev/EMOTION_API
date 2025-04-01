from datetime import datetime, timedelta
from typing import List, Dict, Optional
import numpy as np
from sklearn.cluster import KMeans
from app.models.user_behavior import (
    UserBehavior, BehaviorPattern, BehaviorInsight,
    UserBehaviorProfile, BehaviorType
)
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class UserBehaviorService:
    def __init__(self):
        self.kmeans = KMeans(n_clusters=3)
        
    async def record_behavior(self, behavior: UserBehavior) -> UserBehaviorProfile:
        """
        记录用户行为并更新行为画像
        """
        # 获取现有行为画像
        profile = await self._get_user_behavior_profile(behavior.user_id)
        
        # 添加新行为记录
        profile.behavior_history.append(behavior)
        
        # 更新行为模式
        await self._update_behavior_patterns(profile)
        
        # 更新行为洞察
        await self._update_behavior_insights(profile)
        
        # 更新时间戳
        profile.last_updated = datetime.utcnow()
        
        # 保存更新后的画像
        await self._save_user_behavior_profile(profile)
        
        return profile
    
    async def get_behavior_insights(self, user_id: str) -> BehaviorInsight:
        """
        获取用户行为洞察
        """
        profile = await self._get_user_behavior_profile(user_id)
        return profile.behavior_insight
    
    async def get_behavior_patterns(self, user_id: str) -> BehaviorPattern:
        """
        获取用户行为模式
        """
        profile = await self._get_user_behavior_profile(user_id)
        return profile.behavior_pattern
    
    async def _update_behavior_patterns(self, profile: UserBehaviorProfile):
        """
        更新行为模式
        """
        # 分析每日模式
        daily_pattern = self._analyze_daily_pattern(profile.behavior_history)
        profile.behavior_pattern.daily_pattern = daily_pattern
        
        # 分析每周模式
        weekly_pattern = self._analyze_weekly_pattern(profile.behavior_history)
        profile.behavior_pattern.weekly_pattern = weekly_pattern
        
        # 分析行为序列
        behavior_sequence = self._analyze_behavior_sequence(profile.behavior_history)
        profile.behavior_pattern.behavior_sequence = behavior_sequence
        
        # 分析行为交互
        interaction_graph = self._analyze_interaction_graph(profile.behavior_history)
        profile.behavior_pattern.interaction_graph = interaction_graph
    
    async def _update_behavior_insights(self, profile: UserBehaviorProfile):
        """
        更新行为洞察
        """
        # 分析活跃时间段
        active_hours = self._analyze_active_hours(profile.behavior_history)
        profile.behavior_insight.active_hours = active_hours
        
        # 分析最常用功能
        favorite_features = self._analyze_favorite_features(profile.behavior_history)
        profile.behavior_insight.favorite_features = favorite_features
        
        # 分析行为聚类
        behavior_clusters = self._analyze_behavior_clusters(profile.behavior_history)
        profile.behavior_insight.behavior_clusters = behavior_clusters
        
        # 计算参与度得分
        engagement_score = self._calculate_engagement_score(profile.behavior_history)
        profile.behavior_insight.engagement_score = engagement_score
        
        # 计算留存率得分
        retention_score = self._calculate_retention_score(profile.behavior_history)
        profile.behavior_insight.retention_score = retention_score
    
    def _analyze_daily_pattern(self, behavior_history: List[UserBehavior]) -> Dict[str, int]:
        """
        分析每日行为模式
        """
        daily_counts = {}
        for behavior in behavior_history:
            hour = behavior.timestamp.hour
            daily_counts[str(hour)] = daily_counts.get(str(hour), 0) + 1
        return daily_counts
    
    def _analyze_weekly_pattern(self, behavior_history: List[UserBehavior]) -> Dict[str, int]:
        """
        分析每周行为模式
        """
        weekly_counts = {}
        for behavior in behavior_history:
            weekday = behavior.timestamp.weekday()
            weekly_counts[str(weekday)] = weekly_counts.get(str(weekday), 0) + 1
        return weekly_counts
    
    def _analyze_behavior_sequence(self, behavior_history: List[UserBehavior]) -> List[Dict[str, float]]:
        """
        分析行为序列模式
        """
        sequences = []
        for i in range(len(behavior_history) - 1):
            current = behavior_history[i].behavior_type
            next_behavior = behavior_history[i + 1].behavior_type
            sequences.append({
                "from": current,
                "to": next_behavior,
                "probability": 1.0  # 简化版本，实际应该计算概率
            })
        return sequences
    
    def _analyze_interaction_graph(self, behavior_history: List[UserBehavior]) -> Dict[str, Dict[str, float]]:
        """
        分析行为交互图
        """
        graph = {}
        for behavior in behavior_history:
            behavior_type = behavior.behavior_type
            if behavior_type not in graph:
                graph[behavior_type] = {}
            
            # 分析与其他行为的关联
            for other_behavior in behavior_history:
                if other_behavior.behavior_type != behavior_type:
                    if other_behavior.behavior_type not in graph[behavior_type]:
                        graph[behavior_type][other_behavior.behavior_type] = 0.0
                    graph[behavior_type][other_behavior.behavior_type] += 1.0
        
        return graph
    
    def _analyze_active_hours(self, behavior_history: List[UserBehavior]) -> List[int]:
        """
        分析活跃时间段
        """
        hour_counts = {}
        for behavior in behavior_history:
            hour = behavior.timestamp.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        # 返回最活跃的3个时间段
        return sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    def _analyze_favorite_features(self, behavior_history: List[UserBehavior]) -> List[str]:
        """
        分析最常用功能
        """
        feature_counts = {}
        for behavior in behavior_history:
            feature = behavior.behavior_type
            feature_counts[feature] = feature_counts.get(feature, 0) + 1
        
        # 返回使用频率最高的5个功能
        return sorted(feature_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _analyze_behavior_clusters(self, behavior_history: List[UserBehavior]) -> List[Dict[str, float]]:
        """
        分析行为聚类
        """
        if not behavior_history:
            return []
            
        # 准备特征数据
        features = []
        for behavior in behavior_history:
            features.append([
                behavior.timestamp.hour,
                behavior.timestamp.weekday(),
                behavior.duration or 0
            ])
        
        features = np.array(features)
        
        # 聚类分析
        clusters = self.kmeans.fit_predict(features)
        
        # 计算每个聚类的特征
        cluster_features = []
        for i in range(3):
            cluster_data = features[clusters == i]
            if len(cluster_data) > 0:
                cluster_features.append({
                    "cluster_id": i,
                    "avg_hour": float(np.mean(cluster_data[:, 0])),
                    "avg_weekday": float(np.mean(cluster_data[:, 1])),
                    "avg_duration": float(np.mean(cluster_data[:, 2]))
                })
        
        return cluster_features
    
    def _calculate_engagement_score(self, behavior_history: List[UserBehavior]) -> float:
        """
        计算参与度得分
        """
        if not behavior_history:
            return 0.0
            
        # 计算最近7天的行为频率
        recent_behaviors = [
            b for b in behavior_history
            if b.timestamp > datetime.utcnow() - timedelta(days=7)
        ]
        
        # 计算得分（0-1）
        score = min(len(recent_behaviors) / 100, 1.0)
        return float(score)
    
    def _calculate_retention_score(self, behavior_history: List[UserBehavior]) -> float:
        """
        计算留存率得分
        """
        if not behavior_history:
            return 0.0
            
        # 计算用户连续活跃天数
        dates = sorted(set(b.timestamp.date() for b in behavior_history))
        if not dates:
            return 0.0
            
        consecutive_days = 1
        current_date = dates[-1]
        
        for date in reversed(dates[:-1]):
            if (current_date - date).days == 1:
                consecutive_days += 1
                current_date = date
            else:
                break
        
        # 计算得分（0-1）
        score = min(consecutive_days / 30, 1.0)
        return float(score)
    
    # 数据库操作方法
    async def _get_user_behavior_profile(self, user_id: str) -> UserBehaviorProfile:
        """从数据库获取用户行为画像"""
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        
        profile_data = await db.user_behaviors.find_one({"user_id": user_id})
        
        if profile_data:
            # 如果找到了用户行为画像数据，就转换为UserBehaviorProfile对象
            return UserBehaviorProfile(**profile_data)
        else:
            # 如果没有找到，创建一个新的空用户行为画像
            current_time = datetime.utcnow()
            new_profile = UserBehaviorProfile(
                user_id=user_id,
                behavior_history=[],
                behavior_pattern=BehaviorPattern(
                    daily_pattern={},
                    weekly_pattern={},
                    behavior_sequence=[],
                    interaction_graph={}
                ),
                behavior_insight=BehaviorInsight(
                    active_hours=[],
                    favorite_features=[],
                    behavior_clusters=[],
                    engagement_score=0.0,
                    retention_score=0.0
                ),
                last_updated=current_time
            )
            
            # 保存到数据库
            await self._save_user_behavior_profile(new_profile)
            
            return new_profile
    
    async def _save_user_behavior_profile(self, profile: UserBehaviorProfile):
        """保存用户行为画像到数据库"""
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        
        # 将UserBehaviorProfile对象转换为字典
        profile_dict = profile.dict(by_alias=True)
        
        # 更新或插入用户行为画像数据
        await db.user_behaviors.update_one(
            {"user_id": profile.user_id},
            {"$set": profile_dict},
            upsert=True
        ) 