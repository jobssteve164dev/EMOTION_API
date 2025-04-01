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
        """分析一天中不同时间段的情绪模式"""
        if not emotion_history:
            return {}
            
        # 将一天分为四个时间段
        time_periods = {
            "morning": (5, 11),    # 5:00-11:59
            "afternoon": (12, 17), # 12:00-17:59
            "evening": (18, 22),   # 18:00-22:59
            "night": (23, 4)       # 23:00-4:59
        }
        
        # 初始化各时间段的情绪数据
        period_emotions = {period: [] for period in time_periods}
        
        # 将情绪记录分配到不同时间段
        for record in emotion_history:
            hour = record.timestamp.hour
            for period, (start, end) in time_periods.items():
                if start <= hour <= end or (period == "night" and (hour >= start or hour <= end)):
                    period_emotions[period].append(record)
        
        # 计算每个时间段的平均情绪强度
        result = {}
        for period, records in period_emotions.items():
            if records:
                # 计算积极情绪和消极情绪的平均强度
                positive_records = [r for r in records if r.emotion_type in ["happy", "excited", "content"]]
                negative_records = [r for r in records if r.emotion_type in ["sad", "angry", "anxious"]]
                
                if positive_records:
                    result[f"{period}_positive"] = sum(r.intensity for r in positive_records) / len(positive_records)
                if negative_records:
                    result[f"{period}_negative"] = sum(r.intensity for r in negative_records) / len(negative_records)
                
                # 计算主导情绪
                emotion_types = [r.emotion_type for r in records]
                if emotion_types:
                    from collections import Counter
                    most_common_emotion = Counter(emotion_types).most_common(1)[0][0]
                    result[f"{period}_dominant"] = most_common_emotion
        
        return result
    
    def _analyze_weekly_pattern(self, emotion_history: List[UserEmotionRecord]) -> Dict[str, float]:
        """分析每周不同日期的情绪模式"""
        if not emotion_history:
            return {}
            
        # 星期名称映射
        weekdays = {
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
            5: "saturday",
            6: "sunday"
        }
        
        # 初始化每天的情绪数据
        day_emotions = {day: [] for day in weekdays.values()}
        
        # 将情绪记录分配到不同日期
        for record in emotion_history:
            weekday = record.timestamp.weekday()
            day_name = weekdays[weekday]
            day_emotions[day_name].append(record)
        
        # 计算每天的情绪指标
        result = {}
        for day, records in day_emotions.items():
            if records:
                # 计算平均情绪强度
                avg_intensity = sum(r.intensity for r in records) / len(records)
                result[f"{day}_intensity"] = avg_intensity
                
                # 计算情绪稳定性（强度的标准差）
                if len(records) > 1:
                    import numpy as np
                    intensities = [r.intensity for r in records]
                    std_intensity = np.std(intensities)
                    result[f"{day}_stability"] = 1 - min(std_intensity, 1)  # 稳定性 = 1 - 标准差
                
                # 计算主导情绪
                emotion_types = [r.emotion_type for r in records]
                if emotion_types:
                    from collections import Counter
                    emotion_counts = Counter(emotion_types)
                    most_common = emotion_counts.most_common(1)[0]
                    result[f"{day}_dominant"] = most_common[0]
                    result[f"{day}_dominant_frequency"] = most_common[1] / len(records)
        
        # 识别情绪最佳和最差的日子
        if result:
            day_avg_intensities = {day: result.get(f"{day}_intensity", 0) for day in weekdays.values()}
            best_day = max(day_avg_intensities.items(), key=lambda x: x[1])
            worst_day = min(day_avg_intensities.items(), key=lambda x: x[1])
            
            result["best_day"] = best_day[0]
            result["worst_day"] = worst_day[0]
        
        return result
    
    def _analyze_triggers(self, emotion_history: List[UserEmotionRecord]) -> Dict[str, float]:
        """分析情绪触发因素"""
        if not emotion_history:
            return {}
            
        # 提取所有情绪记录中的上下文
        all_contexts = [r.context for r in emotion_history if r.context]
        if not all_contexts:
            return {}
            
        # 使用自然语言处理提取关键词
        # 简化版：我们通过分词和计数来识别常见触发因素
        from collections import Counter
        import re
        
        # 将上下文拆分为关键词
        words = []
        for context in all_contexts:
            # 简单分词：按空格和标点符号分割
            context_words = re.findall(r'\w+', context.lower())
            words.extend(context_words)
        
        # 过滤掉常见停用词
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
        
        if not filtered_words:
            return {}
            
        # 计算词频，找出最常见的触发因素
        word_counts = Counter(filtered_words)
        common_triggers = word_counts.most_common(10)  # 获取前10个最常见的词语
        
        # 关联情绪类型与触发因素
        emotion_triggers = {}
        for trigger, _ in common_triggers:
            # 查找含有该触发因素的记录
            trigger_records = [r for r in emotion_history if r.context and trigger in r.context.lower()]
            if trigger_records:
                # 计算该触发因素与各种情绪类型的关联度
                emotion_counts = Counter([r.emotion_type for r in trigger_records])
                total = len(trigger_records)
                
                # 找出最相关的情绪
                most_common_emotion = emotion_counts.most_common(1)[0]
                emotion_triggers[trigger] = {
                    "frequency": len(trigger_records) / len(emotion_history),
                    "primary_emotion": most_common_emotion[0],
                    "primary_emotion_strength": most_common_emotion[1] / total,
                    "avg_intensity": sum(r.intensity for r in trigger_records) / len(trigger_records)
                }
        
        # 重新组织结果格式
        result = {}
        for trigger, data in emotion_triggers.items():
            result[trigger] = data["frequency"]
            result[f"{trigger}_emotion"] = data["primary_emotion"]
            result[f"{trigger}_strength"] = data["primary_emotion_strength"]
            result[f"{trigger}_intensity"] = data["avg_intensity"]
            
        return result
    
    def _analyze_coping_strategies(self, emotion_history: List[UserEmotionRecord]) -> Dict[str, float]:
        """分析用户应对负面情绪的策略及其效果"""
        if not emotion_history:
            return {}
            
        # 找出负面情绪记录及其后续的情绪记录
        negative_emotions = ["sad", "angry", "anxious", "fear", "frustrated", "stressed"]
        
        # 按时间顺序排序情绪历史
        sorted_history = sorted(emotion_history, key=lambda x: x.timestamp)
        
        # 分析情绪转变
        transitions = {}
        for i in range(len(sorted_history) - 1):
            current_record = sorted_history[i]
            next_record = sorted_history[i + 1]
            
            # 只关注从负面情绪转变的情况
            if current_record.emotion_type in negative_emotions:
                time_diff = (next_record.timestamp - current_record.timestamp).total_seconds() / 3600
                
                # 只考虑合理时间窗口内的转变(例如24小时内)
                if time_diff <= 24:
                    # 提取当前记录的策略
                    strategy = current_record.coping_strategy if hasattr(current_record, 'coping_strategy') else None
                    
                    # 如果没有明确的策略，尝试从上下文中提取
                    if not strategy and current_record.context:
                        # 一些常见的应对策略关键词
                        strategy_keywords = {
                            "运动": ["跑步", "健身", "散步", "锻炼", "运动"],
                            "社交": ["聊天", "交流", "朋友", "社交", "通话"],
                            "娱乐": ["电影", "音乐", "游戏", "娱乐", "看书", "阅读"],
                            "放松": ["冥想", "休息", "睡觉", "放松", "休闲"],
                            "工作": ["工作", "学习", "忙碌", "专注"],
                            "表达": ["倾诉", "表达", "写作", "日记"]
                        }
                        
                        for strat, keywords in strategy_keywords.items():
                            if any(keyword in current_record.context for keyword in keywords):
                                strategy = strat
                                break
                    
                    # 如果找到策略，分析其效果
                    if strategy:
                        # 计算情绪变化
                        if current_record.emotion_type in negative_emotions and next_record.emotion_type not in negative_emotions:
                            # 从负面到正面：有效
                            effect = 1.0
                        elif current_record.intensity > next_record.intensity and current_record.emotion_type in negative_emotions:
                            # 负面情绪强度降低：部分有效
                            effect = (current_record.intensity - next_record.intensity) / current_record.intensity
                        else:
                            # 无效或负面情绪加剧
                            effect = 0.0
                            
                        # 记录策略及其效果
                        if strategy not in transitions:
                            transitions[strategy] = []
                        transitions[strategy].append(effect)
        
        # 汇总策略效果
        result = {}
        for strategy, effects in transitions.items():
            if effects:
                result[strategy] = sum(effects) / len(effects)
                result[f"{strategy}_count"] = len(effects)
        
        return result
    
    def _analyze_personality(self, emotion_history: List[UserEmotionRecord]) -> Dict[str, float]:
        """基于情绪历史分析用户性格特征"""
        if not emotion_history or len(emotion_history) < 5:
            # 默认中等水平的性格特征
            return {
                "openness": 0.5,
                "conscientiousness": 0.5,
                "extraversion": 0.5,
                "agreeableness": 0.5,
                "neuroticism": 0.5
            }
        
        # 计算情绪类型分布
        emotion_counts = {}
        for record in emotion_history:
            emotion_type = record.emotion_type
            if emotion_type not in emotion_counts:
                emotion_counts[emotion_type] = 0
            emotion_counts[emotion_type] += 1
        
        total_records = len(emotion_history)
        emotion_distribution = {k: v / total_records for k, v in emotion_counts.items()}
        
        # 计算情绪变化频率
        sorted_history = sorted(emotion_history, key=lambda x: x.timestamp)
        emotion_changes = sum(1 for i in range(len(sorted_history) - 1) 
                            if sorted_history[i].emotion_type != sorted_history[i+1].emotion_type)
        emotion_change_rate = emotion_changes / (len(sorted_history) - 1) if len(sorted_history) > 1 else 0
        
        # 计算情绪强度平均值和标准差
        intensities = [record.intensity for record in emotion_history]
        avg_intensity = sum(intensities) / len(intensities)
        import numpy as np
        std_intensity = np.std(intensities)
        
        # 计算负面情绪的比例
        negative_emotions = ["sad", "angry", "anxious", "fear", "frustrated", "stressed"]
        negative_count = sum(1 for record in emotion_history if record.emotion_type in negative_emotions)
        negative_ratio = negative_count / total_records
        
        # 计算社交情境中的情绪
        social_contexts = ["社交", "朋友", "聚会", "交流", "聊天", "群组", "团队", "会议"]
        social_records = [r for r in emotion_history if r.context and any(context in r.context for context in social_contexts)]
        social_intensity = sum(r.intensity for r in social_records) / len(social_records) if social_records else 0.5
        
        # 基于以上指标估计五大性格特质
        # 开放性: 情绪变化率、情绪类型多样性
        emotion_variety = len(emotion_counts) / 8  # 假设有8种可能的情绪类型
        openness = (emotion_change_rate * 0.5 + emotion_variety * 0.5) * 0.8 + 0.1  # 归一化到0.1-0.9范围
        
        # 尽责性: 情绪稳定性、低负面情绪比例
        stability = 1 - std_intensity
        conscientiousness = (stability * 0.7 + (1 - negative_ratio) * 0.3) * 0.8 + 0.1
        
        # 外向性: 社交情境中的情绪强度、积极情绪占比
        positive_ratio = 1 - negative_ratio
        extraversion = (social_intensity * 0.6 + positive_ratio * 0.4) * 0.8 + 0.1
        
        # 宜人性: 低愤怒情绪比例、积极社交情绪
        anger_ratio = emotion_distribution.get("angry", 0)
        agreeableness = ((1 - anger_ratio * 3) * 0.5 + positive_ratio * 0.5) * 0.8 + 0.1
        agreeableness = max(0.1, min(0.9, agreeableness))  # 确保在合理范围
        
        # 神经质: 负面情绪比例、情绪波动性
        neuroticism = (negative_ratio * 0.6 + std_intensity * 0.4) * 0.8 + 0.1
        
        return {
            "openness": round(openness, 2),
            "conscientiousness": round(conscientiousness, 2),
            "extraversion": round(extraversion, 2),
            "agreeableness": round(agreeableness, 2),
            "neuroticism": round(neuroticism, 2)
        }
    
    def _analyze_interests(self, emotion_history: List[UserEmotionRecord]) -> Dict:
        """分析用户兴趣偏好"""
        if not emotion_history:
            return {
                "activities": [],
                "preferences": {},
                "emotional_responses": {}
            }
            
        # 预定义的活动类别
        activity_categories = {
            "体育运动": ["跑步", "健身", "游泳", "篮球", "足球", "羽毛球", "乒乓球", "瑜伽", "骑行", "登山", "健走"],
            "艺术文化": ["阅读", "写作", "绘画", "摄影", "音乐", "电影", "戏剧", "舞蹈", "手工", "博物馆", "展览"],
            "社交活动": ["聚会", "聊天", "约会", "团建", "交友", "社区活动", "志愿服务"],
            "休闲娱乐": ["游戏", "旅行", "购物", "烹饪", "美食", "园艺", "钓鱼", "宠物", "收藏", "冥想"],
            "学习工作": ["学习", "工作", "研究", "讲座", "培训", "编程", "语言学习", "技能培训"]
        }
        
        # 扁平化活动关键词列表
        activity_keywords = {}
        for category, activities in activity_categories.items():
            for activity in activities:
                activity_keywords[activity] = category
                
        # 从情绪记录上下文中提取活动
        activities_found = {}
        for record in emotion_history:
            if not record.context:
                continue
                
            # 检查上下文中是否包含活动关键词
            for activity, category in activity_keywords.items():
                if activity in record.context:
                    if activity not in activities_found:
                        activities_found[activity] = {
                            "category": category,
                            "count": 0,
                            "total_intensity": 0,
                            "emotions": {}
                        }
                    
                    activities_found[activity]["count"] += 1
                    activities_found[activity]["total_intensity"] += record.intensity
                    
                    # 记录该活动相关的情绪
                    emotion = record.emotion_type
                    if emotion not in activities_found[activity]["emotions"]:
                        activities_found[activity]["emotions"][emotion] = 0
                    activities_found[activity]["emotions"][emotion] += 1
        
        # 计算活动偏好和情绪响应
        preferences = {}
        emotional_responses = {}
        activities = []
        
        for activity, data in activities_found.items():
            if data["count"] >= 2:  # 只考虑出现至少两次的活动
                # 计算活动偏好分数 (出现频率和情绪强度的加权平均)
                frequency = data["count"] / len(emotion_history)
                avg_intensity = data["total_intensity"] / data["count"]
                preference_score = frequency * 0.4 + avg_intensity * 0.6
                
                # 保存结果
                activities.append(activity)
                preferences[activity] = round(preference_score, 2)
                
                # 计算情绪响应 (活动引起的主要情绪)
                if data["emotions"]:
                    main_emotion = max(data["emotions"].items(), key=lambda x: x[1])[0]
                    emotional_responses[activity] = main_emotion
        
        return {
            "activities": activities,
            "preferences": preferences,
            "emotional_responses": emotional_responses
        }
    
    def _get_prediction_factors(self, features: np.ndarray) -> Dict[str, float]:
        """获取影响情绪预测的关键因素及其权重"""
        if not hasattr(self.emotion_classifier, 'feature_importances_'):
            # 如果模型没有特征重要性，返回一个简化的版本
            return {
                "time_of_day": 0.2,
                "recent_emotions": 0.3,
                "personality": 0.2,
                "context": 0.3
            }
        
        # 获取模型特征重要性
        importances = self.emotion_classifier.feature_importances_
        
        # 特征名称列表 (应与_prepare_prediction_features中的特征顺序一致)
        feature_names = [
            "time_sin", "time_cos",           # 时间特征
            "recent_emotion_1", "recent_emotion_2", "recent_emotion_3",
            "recent_emotion_4", "recent_emotion_5",  # 最近5次情绪
            "openness", "conscientiousness", "extraversion",
            "agreeableness", "neuroticism",   # 性格特征
            "time_of_day", "day_of_week", "weather_score"  # 上下文特征
        ]
        
        # 将特征重要性与特征名称匹配
        raw_factors = {}
        for i, importance in enumerate(importances):
            if i < len(feature_names):
                raw_factors[feature_names[i]] = importance
        
        # 对特征进行分组
        grouped_factors = {
            "time_of_day": raw_factors.get("time_sin", 0) + raw_factors.get("time_cos", 0),
            "recent_emotions": sum(raw_factors.get(f"recent_emotion_{i}", 0) for i in range(1, 6)),
            "personality": sum(raw_factors.get(trait, 0) for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]),
            "context": sum(raw_factors.get(ctx, 0) for ctx in ["time_of_day", "day_of_week", "weather_score"])
        }
        
        # 归一化因素权重
        total_weight = sum(grouped_factors.values())
        if total_weight > 0:
            normalized_factors = {k: v / total_weight for k, v in grouped_factors.items()}
        else:
            normalized_factors = {k: 1.0 / len(grouped_factors) for k in grouped_factors}
        
        # 四舍五入到两位小数
        return {k: round(v, 2) for k, v in normalized_factors.items()} 