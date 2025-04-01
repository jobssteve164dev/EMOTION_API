from datetime import datetime, timedelta
from typing import List, Dict, Optional
import numpy as np
from app.models.social_emotion import (
    SocialEmotionRecord, SocialEmotionAnalysis,
    SocialEmotionTrend, SocialEmotionInsight,
    InteractionType
)

class SocialEmotionService:
    def __init__(self):
        self.emotion_weights = {
            "positive": 1.0,
            "negative": -1.0,
            "neutral": 0.0
        }
        
        self.interaction_weights = {
            InteractionType.CHAT: 0.3,
            InteractionType.COMMENT: 0.2,
            InteractionType.LIKE: 0.1,
            InteractionType.SHARE: 0.2,
            InteractionType.FOLLOW: 0.1,
            InteractionType.UNFOLLOW: -0.1,
            InteractionType.MENTION: 0.2
        }
    
    async def record_social_interaction(self, record: SocialEmotionRecord) -> SocialEmotionRecord:
        """
        记录社交互动
        """
        # TODO: 实现数据库存储
        return record
    
    async def analyze_social_emotion(self, user_id: str) -> SocialEmotionAnalysis:
        """
        分析用户社交情绪
        """
        # 获取最近的社交互动记录
        recent_records = await self._get_recent_interactions(user_id)
        
        # 计算社交情绪得分
        emotion_score = self._calculate_emotion_score(recent_records)
        
        # 计算社交参与度
        engagement = self._calculate_engagement(recent_records)
        
        # 计算社交网络规模
        network_size = self._calculate_network_size(user_id)
        
        # 分析互动模式
        interaction_patterns = self._analyze_interaction_patterns(recent_records)
        
        # 计算情绪传染度
        emotional_contagion = self._calculate_emotional_contagion(recent_records)
        
        return SocialEmotionAnalysis(
            user_id=user_id,
            social_emotion_score=emotion_score,
            social_engagement=engagement,
            social_network_size=network_size,
            interaction_patterns=interaction_patterns,
            emotional_contagion=emotional_contagion
        )
    
    async def get_social_emotion_trend(self, user_id: str, time_period: str) -> SocialEmotionTrend:
        """
        获取社交情绪趋势
        """
        # 根据时间周期获取数据
        records = await self._get_period_records(user_id, time_period)
        
        # 计算情绪得分趋势
        emotion_scores = self._calculate_emotion_trend(records)
        
        # 计算参与度趋势
        engagement_scores = self._calculate_engagement_trend(records)
        
        # 计算网络增长趋势
        network_growth = self._calculate_network_growth(user_id, time_period)
        
        # 计算互动数量趋势
        interaction_counts = self._calculate_interaction_counts(records)
        
        # 获取时间戳列表
        timestamps = self._get_timestamps(records)
        
        return SocialEmotionTrend(
            user_id=user_id,
            time_period=time_period,
            emotion_scores=emotion_scores,
            engagement_scores=engagement_scores,
            network_growth=network_growth,
            interaction_counts=interaction_counts,
            timestamps=timestamps
        )
    
    async def get_social_emotion_insights(self, user_id: str) -> SocialEmotionInsight:
        """
        获取社交情绪洞察
        """
        # 获取最近的社交互动记录
        recent_records = await self._get_recent_interactions(user_id)
        
        # 分析最频繁的互动类型
        top_interactions = self._analyze_top_interactions(recent_records)
        
        # 分析不同互动对情绪的影响
        emotional_impact = self._analyze_emotional_impact(recent_records)
        
        # 计算社交支持度
        social_support = self._calculate_social_support(recent_records)
        
        # 计算社交压力
        social_stress = self._calculate_social_stress(recent_records)
        
        # 分析关系质量
        relationship_quality = self._analyze_relationship_quality(user_id)
        
        return SocialEmotionInsight(
            user_id=user_id,
            top_interactions=top_interactions,
            emotional_impact=emotional_impact,
            social_support=social_support,
            social_stress=social_stress,
            relationship_quality=relationship_quality
        )
    
    def _calculate_emotion_score(self, records: List[SocialEmotionRecord]) -> float:
        """计算社交情绪得分"""
        if not records:
            return 0.0
            
        weighted_scores = []
        for record in records:
            emotion_weight = self.emotion_weights.get(record.emotion_type, 0.0)
            interaction_weight = self.interaction_weights.get(record.interaction_type, 0.0)
            weighted_score = emotion_weight * interaction_weight * record.intensity
            weighted_scores.append(weighted_score)
        
        return float(np.mean(weighted_scores))
    
    def _calculate_engagement(self, records: List[SocialEmotionRecord]) -> float:
        """计算社交参与度"""
        if not records:
            return 0.0
            
        # 计算互动频率
        interaction_frequency = len(records) / 30  # 假设30天为基准
        
        # 计算互动多样性
        interaction_types = set(record.interaction_type for record in records)
        diversity = len(interaction_types) / len(InteractionType)
        
        # 计算情绪投入度
        emotional_investment = np.mean([record.intensity for record in records])
        
        # 综合计算参与度
        engagement = (interaction_frequency * 0.4 + 
                     diversity * 0.3 + 
                     emotional_investment * 0.3)
        
        return float(min(engagement, 1.0))
    
    def _calculate_network_size(self, user_id: str) -> int:
        """计算社交网络规模"""
        # TODO: 实现从数据库获取社交网络规模
        return 100
    
    def _analyze_interaction_patterns(self, records: List[SocialEmotionRecord]) -> Dict[str, float]:
        """分析互动模式"""
        patterns = {}
        total_interactions = len(records)
        
        if total_interactions == 0:
            return patterns
            
        for interaction_type in InteractionType:
            type_count = sum(1 for r in records if r.interaction_type == interaction_type)
            patterns[interaction_type] = type_count / total_interactions
            
        return patterns
    
    def _calculate_emotional_contagion(self, records: List[SocialEmotionRecord]) -> float:
        """计算情绪传染度"""
        if not records:
            return 0.0
            
        # 计算情绪一致性
        emotions = [record.emotion_type for record in records]
        unique_emotions = set(emotions)
        emotion_counts = {e: emotions.count(e) for e in unique_emotions}
        max_count = max(emotion_counts.values())
        consistency = max_count / len(emotions)
        
        # 计算情绪强度
        intensity = np.mean([record.intensity for record in records])
        
        # 综合计算情绪传染度
        contagion = consistency * intensity
        
        return float(contagion)
    
    async def _get_recent_interactions(self, user_id: str) -> List[SocialEmotionRecord]:
        """获取最近的社交互动记录"""
        # 模拟从数据库获取记录
        # 在实际实现中，这里应该是从数据库查询的代码
        now = datetime.now()
        one_month_ago = now - timedelta(days=30)
        
        # 模拟数据
        return [
            SocialEmotionRecord(
                user_id=user_id,
                interaction_type=InteractionType.CHAT,
                target_user_id=f"user_{i}",
                emotion_type="positive" if i % 3 == 0 else ("negative" if i % 3 == 1 else "neutral"),
                intensity=0.7 + (i % 3) * 0.1,
                context="日常聊天",
                timestamp=now - timedelta(days=i % 30, hours=i % 24)
            )
            for i in range(20)
        ]
    
    async def _get_period_records(self, user_id: str, time_period: str) -> List[SocialEmotionRecord]:
        """获取指定时间周期的记录"""
        now = datetime.now()
        
        # 根据时间周期确定起始时间
        if time_period == "day":
            start_time = now - timedelta(days=1)
            interval_hours = 1
            num_points = 24
        elif time_period == "week":
            start_time = now - timedelta(days=7)
            interval_hours = 24
            num_points = 7
        elif time_period == "month":
            start_time = now - timedelta(days=30)
            interval_hours = 24
            num_points = 30
        else:  # year
            start_time = now - timedelta(days=365)
            interval_hours = 24 * 7
            num_points = 52
        
        # 模拟数据
        return [
            SocialEmotionRecord(
                user_id=user_id,
                interaction_type=InteractionType.CHAT if i % 4 == 0 else 
                              (InteractionType.COMMENT if i % 4 == 1 else 
                               (InteractionType.LIKE if i % 4 == 2 else InteractionType.SHARE)),
                target_user_id=f"user_{i % 10}",
                emotion_type="positive" if i % 3 == 0 else ("negative" if i % 3 == 1 else "neutral"),
                intensity=0.7 + (i % 3) * 0.1,
                context="日常互动",
                timestamp=start_time + timedelta(hours=i * interval_hours)
            )
            for i in range(num_points)
        ]
    
    def _calculate_emotion_trend(self, records: List[SocialEmotionRecord]) -> List[float]:
        """计算情绪得分趋势"""
        if not records:
            return []
            
        # 按时间排序
        sorted_records = sorted(records, key=lambda r: r.timestamp)
        
        # 按天分组
        days_records = {}
        for record in sorted_records:
            day_key = record.timestamp.strftime('%Y-%m-%d')
            if day_key not in days_records:
                days_records[day_key] = []
            days_records[day_key].append(record)
        
        # 计算每天的情绪得分
        emotion_scores = []
        for day, day_records in days_records.items():
            day_score = self._calculate_emotion_score(day_records)
            emotion_scores.append(day_score)
        
        return emotion_scores
    
    def _calculate_engagement_trend(self, records: List[SocialEmotionRecord]) -> List[float]:
        """计算参与度趋势"""
        if not records:
            return []
            
        # 按时间排序
        sorted_records = sorted(records, key=lambda r: r.timestamp)
        
        # 按天分组
        days_records = {}
        for record in sorted_records:
            day_key = record.timestamp.strftime('%Y-%m-%d')
            if day_key not in days_records:
                days_records[day_key] = []
            days_records[day_key].append(record)
        
        # 计算每天的参与度
        engagement_scores = []
        for day, day_records in days_records.items():
            day_engagement = self._calculate_engagement(day_records)
            engagement_scores.append(day_engagement)
        
        return engagement_scores
    
    def _calculate_network_growth(self, user_id: str, time_period: str) -> List[int]:
        """计算网络增长趋势"""
        # 模拟数据 - 根据时间周期生成网络增长数据
        start_size = 100
        
        if time_period == "day":
            num_points = 24
            growth_rate = 0.01
        elif time_period == "week":
            num_points = 7
            growth_rate = 0.03
        elif time_period == "month":
            num_points = 30
            growth_rate = 0.05
        else:  # year
            num_points = 12
            growth_rate = 0.1
        
        result = []
        current_size = start_size
        
        for i in range(num_points):
            # 添加一些随机波动
            random_factor = 1 + (np.random.random() - 0.5) * 0.02
            current_size = int(current_size * (1 + growth_rate * random_factor))
            result.append(current_size)
        
        return result
    
    def _calculate_interaction_counts(self, records: List[SocialEmotionRecord]) -> Dict[str, List[int]]:
        """计算互动数量趋势"""
        if not records:
            return {}
            
        # 按时间排序
        sorted_records = sorted(records, key=lambda r: r.timestamp)
        
        # 按天分组
        days_records = {}
        for record in sorted_records:
            day_key = record.timestamp.strftime('%Y-%m-%d')
            if day_key not in days_records:
                days_records[day_key] = []
            days_records[day_key].append(record)
        
        # 初始化结果字典
        result = {interaction_type.value: [] for interaction_type in InteractionType}
        
        # 计算每种互动类型的每日计数
        for day, day_records in days_records.items():
            # 计算每种互动类型的计数
            type_counts = {}
            for interaction_type in InteractionType:
                type_counts[interaction_type.value] = sum(1 for r in day_records if r.interaction_type == interaction_type)
            
            # 将计数添加到结果中
            for interaction_type in InteractionType:
                result[interaction_type.value].append(type_counts[interaction_type.value])
        
        return result
    
    def _get_timestamps(self, records: List[SocialEmotionRecord]) -> List[datetime]:
        """获取时间戳列表"""
        return [record.timestamp for record in records]
    
    def _analyze_top_interactions(self, records: List[SocialEmotionRecord]) -> List[Dict[str, float]]:
        """分析最频繁的互动类型"""
        if not records:
            return []
            
        # 计算每种互动类型的频率和情绪影响
        interaction_stats = {}
        for interaction_type in InteractionType:
            type_records = [r for r in records if r.interaction_type == interaction_type]
            frequency = len(type_records) / len(records) if records else 0
            
            # 计算情绪影响
            if type_records:
                emotional_impact = np.mean([
                    self.emotion_weights.get(r.emotion_type, 0.0) * r.intensity 
                    for r in type_records
                ])
            else:
                emotional_impact = 0.0
            
            interaction_stats[interaction_type] = {
                "frequency": frequency,
                "emotional_impact": emotional_impact
            }
        
        # 按频率排序并取前3个
        sorted_interactions = sorted(
            interaction_stats.items(),
            key=lambda x: x[1]["frequency"],
            reverse=True
        )[:3]
        
        # 格式化结果
        result = []
        for interaction_type, stats in sorted_interactions:
            result.append({
                "type": interaction_type.value,
                "frequency": stats["frequency"],
                "emotional_impact": stats["emotional_impact"]
            })
        
        return result
    
    def _analyze_emotional_impact(self, records: List[SocialEmotionRecord]) -> Dict[str, float]:
        """分析不同互动对情绪的影响"""
        if not records:
            return {}
            
        result = {}
        for interaction_type in InteractionType:
            type_records = [r for r in records if r.interaction_type == interaction_type]
            
            if type_records:
                # 计算情绪影响值
                impact = np.mean([
                    self.emotion_weights.get(r.emotion_type, 0.0) * r.intensity 
                    for r in type_records
                ])
                # 归一化到0-1范围
                impact = (impact + 1) / 2
                result[interaction_type.value] = impact
            else:
                result[interaction_type.value] = 0.5  # 中性影响
        
        return result
    
    def _calculate_social_support(self, records: List[SocialEmotionRecord]) -> float:
        """计算社交支持度"""
        if not records:
            return 0.5  # 默认中等支持度
            
        # 提取积极互动
        positive_records = [
            r for r in records 
            if r.emotion_type == "positive" and 
            r.interaction_type in [InteractionType.CHAT, InteractionType.COMMENT]
        ]
        
        # 计算积极互动的比例
        positive_ratio = len(positive_records) / len(records) if records else 0
        
        # 计算互动强度
        if positive_records:
            avg_intensity = np.mean([r.intensity for r in positive_records])
        else:
            avg_intensity = 0
        
        # 计算社交支持度
        support = positive_ratio * 0.7 + avg_intensity * 0.3
        
        return float(min(support, 1.0))
    
    def _calculate_social_stress(self, records: List[SocialEmotionRecord]) -> float:
        """计算社交压力"""
        if not records:
            return 0.2  # 默认较低压力
            
        # 提取负面互动
        negative_records = [
            r for r in records 
            if r.emotion_type == "negative"
        ]
        
        # 计算负面互动的比例
        negative_ratio = len(negative_records) / len(records) if records else 0
        
        # 计算负面互动强度
        if negative_records:
            avg_intensity = np.mean([r.intensity for r in negative_records])
        else:
            avg_intensity = 0
        
        # 计算社交压力
        stress = negative_ratio * 0.7 + avg_intensity * 0.3
        
        return float(min(stress, 1.0))
    
    def _analyze_relationship_quality(self, user_id: str) -> Dict[str, float]:
        """分析关系质量"""
        # 在实际实现中，这应该从数据库读取关系数据
        # 这里返回模拟数据
        return {
            "family": 0.9,
            "friends": 0.85,
            "colleagues": 0.75,
            "acquaintances": 0.6
        } 