# 情感分析引擎 SDK 文档

## 安装

```bash
pip install emotion-sdk
```

## 初始化

```python
from emotion_sdk import EmotionSDK

# 初始化SDK
sdk = EmotionSDK(
    base_url="http://your-api-url",
    api_key="your-api-key"  # 可选
)
```

## 认证

### 登录
```python
# 登录获取访问令牌
success = sdk.login(
    username="your_username",
    password="your_password"
)

if success:
    print("登录成功")
else:
    print("登录失败")
```

## 情绪分析

### 分析文本情感
```python
# 分析文本情感
result = sdk.analyze_emotion("今天天气真好，我很开心！")

print(f"情感得分: {result['analysis']['score']}")
print(f"主要情绪: {result['analysis']['emotion']}")
print(f"置信度: {result['analysis']['confidence']}")
print("建议:")
for suggestion in result['suggestions']:
    print(f"- {suggestion}")
```

### 获取情感历史
```python
from datetime import datetime, timedelta

# 获取最近30天的情感历史
history = sdk.get_emotion_history(
    user_id="user_123",
    start_date=datetime.now() - timedelta(days=30)
)

for record in history:
    print(f"时间: {record['timestamp']}")
    print(f"情绪: {record['emotion_type']}")
    print(f"强度: {record['intensity']}")
    print("---")
```

### 获取情感趋势
```python
# 获取最近30天的情感趋势
trend = sdk.get_emotion_trend(
    user_id="user_123",
    days=30
)

print(f"平均情绪得分: {trend['average_score']}")
print(f"情绪稳定性: {trend['stability']}")
```

## 用户画像

### 获取综合用户画像
```python
# 获取综合用户画像
profile = sdk.get_comprehensive_profile("user_123")

print("基本信息:")
print(f"- 年龄: {profile['basic_info']['age']}")
print(f"- 职业: {profile['basic_info']['occupation']}")

print("\n情绪画像:")
print(f"- 当前情绪: {profile['emotional_profile']['current_emotion']}")
print(f"- 情绪稳定性: {profile['emotional_profile']['emotion_stability']}")
print("主要情绪:")
for emotion, ratio in profile['emotional_profile']['dominant_emotions'].items():
    print(f"- {emotion}: {ratio}")

print("\n社交画像:")
print(f"- 社交网络规模: {profile['social_profile']['social_network_size']}")
print(f"- 社交参与度: {profile['social_profile']['social_engagement']}")
print("关系质量:")
for relation, quality in profile['social_profile']['relationship_quality'].items():
    print(f"- {relation}: {quality}")

print("\n行为画像:")
print("活跃时段:")
for hour in profile['behavior_profile']['active_hours']:
    print(f"- {hour}:00")
print("偏好活动:")
for activity, ratio in profile['behavior_profile']['preferred_activities'].items():
    print(f"- {activity}: {ratio}")

print("\n风险画像:")
print(f"- 预警级别: {profile['risk_profile']['alert_level']}")
print(f"- 活动预警数: {profile['risk_profile']['active_alerts']}")
print("风险因素:")
for factor in profile['risk_profile']['risk_factors']:
    print(f"- {factor['type']}: {factor['level']}")

print("\n建议:")
for category, suggestions in profile['recommendations'].items():
    print(f"\n{category}:")
    for suggestion in suggestions:
        print(f"- {suggestion}")
```

### 获取用户画像洞察报告
```python
# 获取用户画像洞察报告
insights = sdk.get_profile_insights(
    user_id="user_123",
    time_period="month"
)

print("情绪洞察:")
print("稳定性趋势:")
for score in insights['emotional_insights']['stability_trend']:
    print(f"- {score}")
print("\n情绪分布:")
for emotion, ratio in insights['emotional_insights']['emotion_distribution'].items():
    print(f"- {emotion}: {ratio}")
print("\n情绪触发因素:")
for emotion, triggers in insights['emotional_insights']['triggers'].items():
    print(f"- {emotion}:")
    for trigger in triggers:
        print(f"  * {trigger}")

print("\n社交洞察:")
print("网络增长趋势:")
for size in insights['social_insights']['network_growth']:
    print(f"- {size}")
print("\n互动质量:")
for type_, quality in insights['social_insights']['interaction_quality'].items():
    print(f"- {type_}: {quality}")

print("\n行为洞察:")
print("活动模式:")
for time, activities in insights['behavior_insights']['activity_patterns'].items():
    print(f"- {time}:")
    for activity in activities:
        print(f"  * {activity}")
print("\n生产力指标:")
for metric, value in insights['behavior_insights']['productivity_metrics'].items():
    print(f"- {metric}: {value}")

print("\n风险洞察:")
print("预警历史:")
for alert in insights['risk_insights']['alert_history']:
    print(f"- 日期: {alert['date']}")
    print(f"  类型: {alert['type']}")
    print(f"  级别: {alert['level']}")
    print(f"  状态: {'已解决' if alert['resolved'] else '未解决'}")
print("\n风险趋势:")
for risk, trend in insights['risk_insights']['risk_trends'].items():
    print(f"- {risk}: {trend}")

print("\n建议:")
print("短期建议:")
for suggestion in insights['recommendations']['short_term']:
    print(f"- {suggestion}")
print("\n长期建议:")
for suggestion in insights['recommendations']['long_term']:
    print(f"- {suggestion}")
```

### 预测用户情绪状态
```python
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

print("\n影响因素:")
print("积极因素:")
for factor in prediction['factors']['positive']:
    print(f"- {factor['factor']}:")
    print(f"  影响程度: {factor['impact']}")
    print(f"  详情: {factor['details']}")

print("\n消极因素:")
for factor in prediction['factors']['negative']:
    print(f"- {factor['factor']}:")
    print(f"  影响程度: {factor['impact']}")
    print(f"  详情: {factor['details']}")

print("\n建议:")
for recommendation in prediction['recommendations']:
    print(f"- {recommendation}")
```

### 记录用户情绪
```python
# 记录用户情绪
record = sdk.record_emotion(
    emotion_type="happy",
    intensity=0.8,
    context="工作完成",
    source="用户反馈",
    text="今天完成了重要项目，很开心！"
)

print(f"记录ID: {record['record_id']}")
print(f"时间戳: {record['timestamp']}")
```

### 获取情绪稳定性
```python
# 获取情绪稳定性指标
stability = sdk.get_emotional_stability()
print(f"情绪稳定性: {stability}")
```

## 用户行为

### 记录用户行为
```python
# 记录用户行为
behavior = sdk.record_behavior(
    action_type="chat",
    duration=300,
    emotion_state="positive",
    context="与朋友聊天"
)

print(f"行为ID: {behavior['behavior_id']}")
print(f"时间戳: {behavior['timestamp']}")
```

### 获取行为洞察
```python
# 获取行为洞察
insights = sdk.get_behavior_insights()

print("活跃时段:")
for hour in insights['active_hours']:
    print(f"- {hour}:00")
print(f"参与度得分: {insights['engagement_score']}")
```

### 获取行为模式
```python
# 获取行为模式
patterns = sdk.get_behavior_patterns()

print("每日模式:")
for hour, count in patterns['daily_pattern'].items():
    print(f"- {hour}:00 - {count}次")
```

## 情绪预警

### 获取预警规则
```python
# 获取预警规则列表
rules = sdk.get_alert_rules()

for rule in rules:
    print(f"规则名称: {rule['name']}")
    print(f"描述: {rule['description']}")
    print(f"级别: {rule['level']}")
    print("条件:")
    for key, value in rule['conditions'].items():
        print(f"- {key}: {value}")
    print("---")
```

### 获取预警历史
```python
# 获取预警历史
history = sdk.get_alert_history()

print(f"总预警数: {history['total_alerts']}")
print(f"活动预警数: {history['active_alerts']}")
print("预警列表:")
for alert in history['alerts']:
    print(f"- ID: {alert['id']}")
    print(f"  级别: {alert['level']}")
    print(f"  消息: {alert['message']}")
    print(f"  状态: {alert['status']}")
    print("  ---")
```

### 解决预警
```python
# 解决预警
alert = sdk.resolve_alert("alert_123")
print(f"预警状态: {alert['status']}")
print(f"解决时间: {alert['resolved_at']}")
```

### 忽略预警
```python
# 忽略预警
alert = sdk.dismiss_alert("alert_123")
print(f"预警状态: {alert['status']}")
```

### 获取预警汇总报告
```python
# 获取预警汇总报告
summary = sdk.get_alert_summary()
print(f"状态: {summary['status']}")
print(f"消息: {summary['message']}")
```

## 社交情绪分析

### 记录社交互动
```python
from datetime import datetime
from emotion_sdk.models import SocialEmotionRecord

# 记录社交互动
record = sdk.record_social_interaction(
    user_id="user_123",
    interaction_type="chat",
    emotion_type="positive",
    intensity=0.8,
    context="与朋友聊天",
    timestamp=datetime.now(),
    interaction_id="interaction_456",
    target_user_id="user_789"
)

print(f"记录ID: {record['id']}")
print(f"时间戳: {record['timestamp']}")
```

### 获取社交情绪分析
```python
# 获取社交情绪分析
analysis = sdk.get_social_emotion_analysis("user_123")

print(f"社交情绪得分: {analysis['social_emotion_score']}")
print(f"社交参与度: {analysis['social_engagement']}")
print(f"社交网络规模: {analysis['social_network_size']}")
print("互动模式:")
for type_, ratio in analysis['interaction_patterns'].items():
    print(f"- {type_}: {ratio}")
print(f"情绪传染度: {analysis['emotional_contagion']}")
```

### 获取社交情绪趋势
```python
# 获取社交情绪趋势
trend = sdk.get_social_emotion_trend(
    user_id="user_123",
    time_period="week"
)

print(f"时间周期: {trend['time_period']}")
print("情绪得分趋势:")
for score in trend['emotion_scores']:
    print(f"- {score}")
print("参与度趋势:")
for score in trend['engagement_scores']:
    print(f"- {score}")
print("网络增长趋势:")
for size in trend['network_growth']:
    print(f"- {size}")
```

### 获取社交情绪洞察
```python
# 获取社交情绪洞察
insights = sdk.get_social_emotion_insights("user_123")

print("最频繁的互动类型:")
for interaction in insights['top_interactions']:
    print(f"- {interaction['type']}: 频率={interaction['frequency']}, 情绪影响={interaction['emotional_impact']}")

print("\n不同互动的情绪影响:")
for type_, impact in insights['emotional_impact'].items():
    print(f"- {type_}: {impact}")

print(f"\n社交支持度: {insights['social_support']}")
print(f"社交压力: {insights['social_stress']}")

print("\n关系质量:")
for relation, quality in insights['relationship_quality'].items():
    print(f"- {relation}: {quality}")
```

## 错误处理

SDK中的方法在发生错误时会抛出异常：

```python
try:
    result = sdk.analyze_emotion("测试文本")
except Exception as e:
    print(f"发生错误: {str(e)}")
```

常见错误类型：
- `AuthenticationError`: 认证失败
- `ValidationError`: 参数验证失败
- `APIError`: API调用失败
- `ConnectionError`: 网络连接失败

## 关闭连接

使用完毕后，建议关闭SDK连接：

```python
# 关闭SDK连接
sdk.close()
``` 