from datetime import datetime, timedelta
from typing import List, Dict, Optional
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from app.models.user_profile import (
    UserProfile, UserEmotionRecord, UserPersonality,
    UserInterests, UserEmotionPattern, EmotionPrediction,
    PersonalizedRecommendation, EmotionType
)

class UserProfileService:
    def __init__(self):
        self.scaler = StandardScaler()
        self.emotion_classifier = RandomForestClassifier()
        
    async def update_user_profile(self, user_id: str, emotion_record: UserEmotionRecord) -> UserProfile:
        """
        更新用户画像
        """
        # 获取现有用户画像
        profile = await self._get_user_profile(user_id)
        
        # 更新情绪历史
        profile.emotion_history.append(emotion_record)
        
        # 更新当前情绪
        profile.current_emotion = emotion_record
        
        # 更新情绪模式
        await self._update_emotion_patterns(profile)
        
        # 更新性格特征
        await self._update_personality(profile)
        
        # 更新兴趣偏好
        await self._update_interests(profile)
        
        # 计算情绪稳定性
        profile.emotional_stability = self._calculate_emotional_stability(profile)
        
        # 更新时间戳
        profile.last_updated = datetime.utcnow()
        
        # 保存更新后的画像
        await self._save_user_profile(profile)
        
        return profile
    
    async def predict_emotion(self, user_id: str, context: Dict) -> EmotionPrediction:
        """
        预测用户当前情绪
        """
        profile = await self._get_user_profile(user_id)
        
        # 准备特征数据
        features = self._prepare_prediction_features(profile, context)
        
        # 预测情绪
        prediction = self._predict_emotion(features)
        
        return EmotionPrediction(
            predicted_emotion=prediction['emotion'],
            confidence=prediction['confidence'],
            factors=prediction['factors'],
            timestamp=datetime.utcnow()
        )
    
    async def generate_recommendations(self, user_id: str, context: Dict) -> List[PersonalizedRecommendation]:
        """
        生成个性化推荐
        """
        profile = await self._get_user_profile(user_id)
        current_emotion = profile.current_emotion
        
        recommendations = []
        
        # 基于当前情绪的推荐
        if current_emotion and current_emotion.intensity < 0.3:
            recommendations.extend(
                self._generate_emotion_improvement_recommendations(profile)
            )
        
        # 基于兴趣的推荐
        recommendations.extend(
            self._generate_interest_based_recommendations(profile)
        )
        
        # 基于时间模式的推荐
        recommendations.extend(
            self._generate_timing_based_recommendations(profile)
        )
        
        # 基于社交情绪的推荐
        if context and "social_score" in context:
            recommendations.extend(
                self._generate_social_recommendations(profile, context)
            )
            
        # 基于风险因素的推荐
        if context and "risk_level" in context:
            recommendations.extend(
                self._generate_risk_prevention_recommendations(profile, context)
            )
        
        # 排序推荐
        recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return recommendations[:5]  # 返回前5个最相关的推荐
    
    async def _update_emotion_patterns(self, profile: UserProfile):
        """
        更新情绪模式
        """
        # 分析每日模式
        daily_pattern = self._analyze_daily_pattern(profile.emotion_history)
        profile.emotion_pattern.daily_pattern = daily_pattern
        
        # 分析每周模式
        weekly_pattern = self._analyze_weekly_pattern(profile.emotion_history)
        profile.emotion_pattern.weekly_pattern = weekly_pattern
        
        # 分析触发因素
        triggers = self._analyze_triggers(profile.emotion_history)
        profile.emotion_pattern.triggers = triggers
        
        # 分析应对策略
        coping_strategies = self._analyze_coping_strategies(profile.emotion_history)
        profile.emotion_pattern.coping_strategies = coping_strategies
    
    async def _update_personality(self, profile: UserProfile):
        """
        更新性格特征
        """
        # 基于情绪历史分析性格特征
        personality_scores = self._analyze_personality(profile.emotion_history)
        profile.personality = UserPersonality(
            **personality_scores,
            last_updated=datetime.utcnow()
        )
    
    async def _update_interests(self, profile: UserProfile):
        """
        更新兴趣偏好
        """
        # 分析用户兴趣
        interests = self._analyze_interests(profile.emotion_history)
        profile.interests = UserInterests(
            **interests,
            last_updated=datetime.utcnow()
        )
    
    def _calculate_emotional_stability(self, profile: UserProfile) -> float:
        """
        计算情绪稳定性指标
        """
        if not profile.emotion_history:
            return 0.5
            
        # 计算情绪波动
        emotions = [record.intensity for record in profile.emotion_history[-30:]]
        if not emotions:
            return 0.5
            
        # 计算标准差
        std = np.std(emotions)
        # 转换为0-1的稳定性指标
        stability = 1 - min(std, 1)
        
        return float(stability)
    
    def _prepare_prediction_features(self, profile: UserProfile, context: Dict) -> np.ndarray:
        """
        准备预测特征
        """
        features = []
        
        # 添加时间特征
        current_hour = datetime.utcnow().hour
        features.extend([
            np.sin(2 * np.pi * current_hour / 24),
            np.cos(2 * np.pi * current_hour / 24)
        ])
        
        # 添加历史情绪特征
        if profile.emotion_history:
            recent_emotions = [record.intensity for record in profile.emotion_history[-5:]]
            features.extend(recent_emotions)
        else:
            features.extend([0.5] * 5)
        
        # 添加性格特征
        features.extend([
            profile.personality.openness,
            profile.personality.conscientiousness,
            profile.personality.extraversion,
            profile.personality.agreeableness,
            profile.personality.neuroticism
        ])
        
        # 添加上下文特征
        features.extend([
            context.get('time_of_day', 0.5),
            context.get('day_of_week', 0.5),
            context.get('weather_score', 0.5)
        ])
        
        return np.array(features).reshape(1, -1)
    
    def _predict_emotion(self, features: np.ndarray) -> Dict:
        """
        预测情绪
        """
        # 标准化特征
        scaled_features = self.scaler.fit_transform(features)
        
        # 预测情绪类型
        prediction = self.emotion_classifier.predict_proba(scaled_features)[0]
        emotion_idx = np.argmax(prediction)
        confidence = prediction[emotion_idx]
        
        # 获取影响因素
        factors = self._get_prediction_factors(features[0])
        
        return {
            'emotion': EmotionType(emotion_idx),
            'confidence': float(confidence),
            'factors': factors
        }
    
    def _generate_emotion_improvement_recommendations(self, profile: UserProfile) -> List[PersonalizedRecommendation]:
        """
        生成情绪改善建议
        """
        recommendations = []
        
        # 基于用户兴趣生成活动建议
        for activity in profile.interests.activities:
            recommendations.append(
                PersonalizedRecommendation(
                    type="activity",
                    content=f"尝试{activity}来改善心情",
                    reason="基于您的兴趣",
                    relevance_score=profile.interests.preferences.get(activity, 0.5),
                    user_context={"current_emotion": profile.current_emotion}
                )
            )
        
        # 基于应对策略生成建议
        for strategy, effectiveness in profile.emotion_pattern.coping_strategies.items():
            if effectiveness > 0.7:
                recommendations.append(
                    PersonalizedRecommendation(
                        type="strategy",
                        content=f"使用{strategy}来调节情绪",
                        reason="基于历史效果",
                        relevance_score=effectiveness,
                        user_context={"current_emotion": profile.current_emotion}
                    )
                )
        
        return recommendations
    
    def _generate_interest_based_recommendations(self, profile: UserProfile) -> List[PersonalizedRecommendation]:
        """
        生成基于兴趣的推荐
        """
        recommendations = []
        
        for topic in profile.interests.topics:
            recommendations.append(
                PersonalizedRecommendation(
                    type="content",
                    content=f"探索{topic}相关的内容",
                    reason="基于您的兴趣",
                    relevance_score=profile.interests.preferences.get(topic, 0.5),
                    user_context={"interests": profile.interests.topics}
                )
            )
        
        return recommendations
    
    def _generate_timing_based_recommendations(self, profile: UserProfile) -> List[PersonalizedRecommendation]:
        """
        生成基于时间模式的推荐
        """
        recommendations = []
        current_hour = datetime.utcnow().hour
        
        # 根据每日模式推荐活动时间
        for hour, intensity in profile.emotion_pattern.daily_pattern.items():
            if abs(int(hour) - current_hour) < 2 and intensity > 0.7:
                recommendations.append(
                    PersonalizedRecommendation(
                        type="timing",
                        content=f"现在是进行{hour}点常做活动的好时机",
                        reason="基于您的日常模式",
                        relevance_score=intensity,
                        user_context={"current_time": current_hour}
                    )
                )
        
        return recommendations
    
    def _generate_social_recommendations(self, profile: UserProfile, context: Dict) -> List[PersonalizedRecommendation]:
        """生成社交健康相关的推荐"""
        recommendations = []
        
        social_score = context.get("social_score", 0.5)
        
        # 根据社交情绪得分提供建议
        if social_score < 0.3:
            # 负面社交情绪时的建议
            recommendations.append(
                PersonalizedRecommendation(
                    type="social",
                    content="尝试与亲近的朋友进行一次深入交流",
                    reason="增强社交联系有助于改善社交情绪",
                    relevance_score=0.85,
                    user_context={"social_score": social_score}
                )
            )
            recommendations.append(
                PersonalizedRecommendation(
                    type="social",
                    content="参加一个小型社交活动，培养新的社交关系",
                    reason="扩展社交圈可以提供新的社交支持",
                    relevance_score=0.75,
                    user_context={"social_score": social_score}
                )
            )
        elif social_score < 0.6:
            # 中等社交情绪时的建议
            recommendations.append(
                PersonalizedRecommendation(
                    type="social",
                    content="定期与朋友保持联系，分享近期经历",
                    reason="保持社交连接有助于维持良好的社交情绪",
                    relevance_score=0.8,
                    user_context={"social_score": social_score}
                )
            )
        else:
            # 良好社交情绪时的建议
            recommendations.append(
                PersonalizedRecommendation(
                    type="social",
                    content="可以尝试组织一次社交活动，分享你的积极体验",
                    reason="分享积极情绪有助于增强社交连接",
                    relevance_score=0.75,
                    user_context={"social_score": social_score}
                )
            )
        
        return recommendations
    
    def _generate_risk_prevention_recommendations(self, profile: UserProfile, context: Dict) -> List[PersonalizedRecommendation]:
        """生成风险预防相关的推荐"""
        recommendations = []
        
        risk_level = context.get("risk_level", "low")
        
        if risk_level == "high":
            recommendations.append(
                PersonalizedRecommendation(
                    type="risk",
                    content="建议进行深呼吸冥想练习，每天10分钟",
                    reason="有助于缓解当前较高的情绪压力",
                    relevance_score=0.9,
                    user_context={"risk_level": risk_level}
                )
            )
            recommendations.append(
                PersonalizedRecommendation(
                    type="risk",
                    content="考虑与专业咨询师交流当前的情绪状态",
                    reason="专业支持有助于应对高风险情绪状态",
                    relevance_score=0.85,
                    user_context={"risk_level": risk_level}
                )
            )
        elif risk_level == "medium":
            recommendations.append(
                PersonalizedRecommendation(
                    type="risk",
                    content="尝试进行30分钟的有氧运动，如散步或慢跑",
                    reason="体育活动有助于调节情绪和减轻压力",
                    relevance_score=0.8,
                    user_context={"risk_level": risk_level}
                )
            )
        else:
            recommendations.append(
                PersonalizedRecommendation(
                    type="risk",
                    content="继续保持健康的生活方式和社交习惯",
                    reason="维持当前的良好状态",
                    relevance_score=0.7,
                    user_context={"risk_level": risk_level}
                )
            )
            
        return recommendations
    
    # 其他辅助方法...
    async def _get_user_profile(self, user_id: str) -> UserProfile:
        """从数据库获取用户画像"""
        # 从MongoDB中查询用户画像
        from motor.motor_asyncio import AsyncIOMotorClient
        from app.core.config import settings
        from uuid import uuid4
        
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        
        profile_data = await db.user_profiles.find_one({"user_id": user_id})
        
        if profile_data:
            # 如果找到了用户画像数据，就转换为UserProfile对象
            return UserProfile(**profile_data)
        else:
            # 如果没有找到，创建一个新的空用户画像
            current_time = datetime.utcnow()
            new_profile = UserProfile(
                user_id=user_id,
                emotional_stability=0.5,
                emotion_history=[],
                current_emotion=None,
                emotion_pattern=UserEmotionPattern(
                    daily_pattern={},
                    weekly_pattern={},
                    triggers={},
                    coping_strategies={}
                ),
                personality=UserPersonality(
                    openness=0.5,
                    conscientiousness=0.5,
                    extraversion=0.5,
                    agreeableness=0.5,
                    neuroticism=0.5,
                    last_updated=current_time
                ),
                interests=UserInterests(
                    activities=[],
                    topics=[],
                    preferences={},
                    last_updated=current_time
                ),
                last_updated=current_time
            )
            
            # 保存到数据库
            await self._save_user_profile(new_profile)
            
            return new_profile
    
    async def _save_user_profile(self, profile: UserProfile):
        """保存用户画像到数据库"""
        from motor.motor_asyncio import AsyncIOMotorClient
        from app.core.config import settings
        
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        
        # 将UserProfile对象转换为字典
        profile_dict = profile.dict(by_alias=True)
        
        # 更新或插入用户画像数据
        await db.user_profiles.update_one(
            {"user_id": profile.user_id},
            {"$set": profile_dict},
            upsert=True
        )
    
    def _analyze_daily_pattern(self, emotion_history: List[UserEmotionRecord]) -> Dict[str, float]:
        """分析每日情绪模式"""
        # TODO: 实现模式分析
        pass
    
    def _analyze_weekly_pattern(self, emotion_history: List[UserEmotionRecord]) -> Dict[str, float]:
        """分析每周情绪模式"""
        # TODO: 实现模式分析
        pass
    
    def _analyze_triggers(self, emotion_history: List[UserEmotionRecord]) -> Dict[str, float]:
        """分析情绪触发因素"""
        # TODO: 实现触发因素分析
        pass
    
    def _analyze_coping_strategies(self, emotion_history: List[UserEmotionRecord]) -> Dict[str, float]:
        """分析应对策略效果"""
        # TODO: 实现策略分析
        pass
    
    def _analyze_personality(self, emotion_history: List[UserEmotionRecord]) -> Dict[str, float]:
        """分析性格特征"""
        # TODO: 实现性格分析
        pass
    
    def _analyze_interests(self, emotion_history: List[UserEmotionRecord]) -> Dict:
        """分析用户兴趣"""
        # TODO: 实现兴趣分析
        pass
    
    def _get_prediction_factors(self, features: np.ndarray) -> Dict[str, float]:
        """获取预测影响因素"""
        # TODO: 实现因素分析
        pass 