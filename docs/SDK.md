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

### 预测用户情绪
```python
# 预测用户当前情绪
prediction = sdk.predict_emotion({
    "time_of_day": 0.5,
    "day_of_week": 1,
    "weather_score": 0.8
})

print(f"预测情绪: {prediction['predicted_emotion']}")
print(f"置信度: {prediction['confidence']}")
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