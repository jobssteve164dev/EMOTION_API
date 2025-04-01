# 情感分析引擎

一个强大的情感分析引擎，提供情绪分析、用户画像、行为分析、情绪预警和社交情绪分析等功能。

## 功能特点

- 文本情感分析
- 用户情绪追踪
- 用户画像构建
- 用户行为分析
- 情绪预警系统
- 个性化推荐
- 社交情绪分析

## 情绪预警系统

情绪预警系统能够实时监测用户的情绪变化，当检测到异常情绪状态时发出预警。主要功能包括：

### 预警规则
- 持续负面情绪检测
- 情绪波动异常检测
- 情绪稳定性下降检测

### 预警级别
- 低级别：轻微情绪波动
- 中级别：情绪波动异常
- 高级别：持续负面情绪
- 严重级别：需要立即干预

### 预警通知
- 实时预警推送
- 预警历史记录
- 预警汇总报告
- 预警处理流程

## 社交情绪分析

社交情绪分析系统能够分析用户在社交互动中的情绪变化和社交关系质量。主要功能包括：

### 社交互动分析
- 记录各类社交互动
- 分析互动模式
- 计算社交参与度
- 评估情绪传染度

### 社交网络分析
- 社交网络规模统计
- 关系质量评估
- 社交支持度分析
- 社交压力评估

### 趋势分析
- 社交情绪趋势
- 参与度趋势
- 网络增长趋势
- 互动数量趋势

### 洞察报告
- 最频繁互动类型
- 情绪影响分析
- 关系质量评估
- 社交健康建议

## 功能特性

### 用户画像
- 综合用户画像分析
  - 情绪画像：情绪状态、稳定性、主要情绪分布
  - 社交画像：社交网络规模、参与度、关系质量
  - 行为画像：活跃时段、偏好活动、行为模式
  - 风险画像：预警级别、活动预警、风险因素
  - 个性化建议：基于多维度分析的建议
- 用户画像洞察报告
  - 情绪洞察：稳定性趋势、情绪分布、触发因素
  - 社交洞察：网络增长、互动质量、关系发展
  - 行为洞察：活动模式、生产力指标、行为变化
  - 风险洞察：预警历史、风险趋势、干预效果
  - 短期和长期建议
- 情绪预测
  - 基于上下文的情绪预测
  - 影响因素分析
  - 个性化建议生成

## 快速开始

### 安装

```bash
pip install emotion-sdk
```

### 使用示例

```python
from emotion_sdk import EmotionSDK
from datetime import datetime

# 初始化SDK
sdk = EmotionSDK(base_url="http://your-api-url")

# 登录
sdk.login(username="your_username", password="your_password")

# 分析文本情感
result = sdk.analyze_emotion("今天天气真好，我很开心！")
print(f"情感分析结果: {result}")

# 记录用户情绪
sdk.record_emotion(
    emotion_type="happy",
    intensity=0.8,
    context="工作完成",
    source="用户反馈"
)

# 记录社交互动
sdk.record_social_interaction(
    user_id="user_123",
    interaction_type="chat",
    emotion_type="positive",
    intensity=0.8,
    context="与朋友聊天",
    timestamp=datetime.now()
)

# 获取社交情绪分析
social_analysis = sdk.get_social_emotion_analysis("user_123")
print(f"社交情绪得分: {social_analysis['social_emotion_score']}")

# 获取预警历史
alerts = sdk.get_alert_history()
print(f"当前活动预警数: {alerts['active_alerts']}")

# 获取综合用户画像
profile = sdk.get_comprehensive_profile("user_123")
print(f"用户情绪稳定性: {profile['emotional_profile']['emotion_stability']}")
print(f"社交参与度: {profile['social_profile']['social_engagement']}")

# 获取用户画像洞察报告
insights = sdk.get_profile_insights("user_123", time_period="month")
print("情绪洞察:")
print(f"稳定性趋势: {insights['emotional_insights']['stability_trend']}")
print(f"情绪分布: {insights['emotional_insights']['emotion_distribution']}")

# 预测用户情绪状态
prediction = sdk.predict_emotion(
    user_id="user_123",
    context={
        "time_of_day": 0.5,
        "day_of_week": 1,
        "weather_score": 0.8,
        "recent_activities": ["work", "exercise"],
        "social_interactions": 3,
        "sleep_quality": 0.9
    }
)
print(f"预测情绪: {prediction['predicted_emotion']}")
print(f"置信度: {prediction['confidence']}")

# 关闭连接
sdk.close()
```# EMOTION_API
