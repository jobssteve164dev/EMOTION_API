# 情感分析引擎 API 文档

## 目录
1. [认证](#认证)
2. [情绪分析](#情绪分析)
3. [用户画像](#用户画像)
4. [用户行为](#用户行为)
5. [情绪预警](#情绪预警)

## 认证

### 获取访问令牌
```http
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

响应：
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

## 情绪分析

### 分析文本情感
```http
POST /api/v1/emotion/analyze
Authorization: Bearer your_token
Content-Type: application/json

{
    "text": "待分析的文本内容"
}
```

响应：
```json
{
    "analysis": {
        "text": "待分析的文本内容",
        "score": 0.85,
        "emotion": "positive",
        "confidence": 0.85,
        "timestamp": "2024-03-31T10:00:00"
    },
    "suggestions": [
        "继续保持积极的心态",
        "分享你的快乐给他人",
        "记录下让你开心的事情"
    ]
}
```

## 用户画像

### 记录用户情绪
```http
POST /api/v1/profile/emotion-record
Authorization: Bearer your_token
Content-Type: application/json

{
    "emotion_type": "happy",
    "intensity": 0.8,
    "context": "工作完成",
    "source": "用户反馈",
    "text": "今天完成了重要项目，很开心！"
}
```

### 预测用户情绪
```http
POST /api/v1/profile/predict-emotion
Authorization: Bearer your_token
Content-Type: application/json

{
    "context": {
        "time_of_day": 0.5,
        "day_of_week": 1,
        "weather_score": 0.8
    }
}
```

### 获取情绪稳定性
```http
GET /api/v1/profile/emotion-stability
Authorization: Bearer your_token
```

## 用户行为

### 记录用户行为
```http
POST /api/v1/behavior/record
Authorization: Bearer your_token
Content-Type: application/json

{
    "action_type": "chat",
    "duration": 300,
    "emotion_state": "positive",
    "context": "与朋友聊天"
}
```

### 获取行为洞察
```http
GET /api/v1/behavior/insights
Authorization: Bearer your_token
```

### 获取行为模式
```http
GET /api/v1/behavior/patterns
Authorization: Bearer your_token
```

## 情绪预警

### 获取预警规则
```http
GET /api/v1/alert/rules
Authorization: Bearer your_token
```

响应：
```json
[
    {
        "id": "rule_1",
        "name": "持续负面情绪",
        "description": "连续3天出现强烈负面情绪",
        "conditions": {
            "negative_intensity_threshold": 0.7,
            "consecutive_days": 3
        },
        "level": "high",
        "enabled": true
    },
    {
        "id": "rule_2",
        "name": "情绪波动异常",
        "description": "24小时内情绪波动超过阈值",
        "conditions": {
            "emotion_volatility_threshold": 0.8,
            "time_window_hours": 24
        },
        "level": "medium",
        "enabled": true
    }
]
```

### 获取预警历史
```http
GET /api/v1/alert/history
Authorization: Bearer your_token
```

响应：
```json
{
    "user_id": "user_123",
    "alerts": [
        {
            "id": "alert_456",
            "user_id": "user_123",
            "rule_id": "rule_1",
            "level": "high",
            "message": "检测到连续3天出现强烈负面情绪",
            "details": {
                "negative_count": 3,
                "average_intensity": 0.85
            },
            "created_at": "2024-03-31T10:00:00",
            "status": "active"
        }
    ],
    "total_alerts": 1,
    "active_alerts": 1,
    "last_alert_time": "2024-03-31T10:00:00"
}
```

### 解决预警
```http
POST /api/v1/alert/resolve/{alert_id}
Authorization: Bearer your_token
```

### 忽略预警
```http
POST /api/v1/alert/dismiss/{alert_id}
Authorization: Bearer your_token
```

### 获取预警汇总报告
```http
GET /api/v1/alert/summary
Authorization: Bearer your_token
```

响应：
```json
{
    "status": "success",
    "message": "汇总报告已发送"
}
```

## 错误响应

所有API在发生错误时会返回以下格式：

```json
{
    "detail": "错误信息描述"
}
```

常见HTTP状态码：
- 200: 请求成功
- 400: 请求参数错误
- 401: 未认证
- 403: 无权限
- 404: 资源不存在
- 500: 服务器内部错误 