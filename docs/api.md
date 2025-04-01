# 情感分析引擎 API 文档

## 目录
1. [认证](#认证)
2. [情绪分析](#情绪分析)
3. [用户画像](#用户画像)
4. [用户行为](#用户行为)
5. [情绪预警](#情绪预警)
6. [社交情绪](#社交情绪)

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

### 获取综合用户画像
```http
GET /api/v1/profile/comprehensive/{user_id}
Authorization: Bearer your_token
```

响应：
```json
{
    "user_id": "user_123",
    "basic_info": {
        "age": 28,
        "gender": "male",
        "occupation": "软件工程师",
        "location": "北京"
    },
    "emotional_profile": {
        "current_emotion": "positive",
        "emotion_stability": 0.85,
        "dominant_emotions": {
            "happy": 0.4,
            "calm": 0.3,
            "excited": 0.2,
            "anxious": 0.1
        },
        "emotion_trend": {
            "positive": 0.75,
            "neutral": 0.15,
            "negative": 0.1
        }
    },
    "social_profile": {
        "social_network_size": 150,
        "social_engagement": 0.85,
        "relationship_quality": {
            "family": 0.9,
            "friends": 0.85,
            "colleagues": 0.75
        },
        "social_support": 0.85,
        "social_stress": 0.2
    },
    "behavior_profile": {
        "active_hours": [9, 10, 11, 14, 15, 16, 20, 21],
        "preferred_activities": {
            "chat": 0.4,
            "work": 0.3,
            "exercise": 0.2,
            "entertainment": 0.1
        },
        "interaction_patterns": {
            "morning": "productive",
            "afternoon": "social",
            "evening": "relaxed"
        }
    },
    "risk_profile": {
        "alert_level": "low",
        "active_alerts": 0,
        "risk_factors": [
            {
                "type": "social_isolation",
                "level": "low",
                "description": "社交互动频率正常"
            }
        ],
        "protective_factors": [
            {
                "type": "strong_social_support",
                "level": "high",
                "description": "有良好的社交支持网络"
            }
        ]
    },
    "recommendations": {
        "emotional_health": [
            "继续保持积极的心态",
            "适当增加户外活动时间"
        ],
        "social_health": [
            "可以尝试参加更多社交活动",
            "建议与朋友保持定期联系"
        ],
        "behavior_improvement": [
            "建议保持规律的作息时间",
            "可以增加运动时间"
        ],
        "risk_prevention": [
            "继续保持良好的社交习惯",
            "注意工作与生活的平衡"
        ]
    },
    "last_updated": "2024-03-31T10:00:00"
}
```

### 获取用户画像洞察报告
```http
GET /api/v1/profile/insights/{user_id}
Authorization: Bearer your_token
Query Parameters:
- time_period: 时间周期（可选值：week, month, quarter, year）
```

响应：
```json
{
    "user_id": "user_123",
    "time_period": "month",
    "emotional_insights": {
        "stability_trend": [0.8, 0.82, 0.85, 0.83, 0.85],
        "emotion_distribution": {
            "positive": 0.75,
            "neutral": 0.15,
            "negative": 0.1
        },
        "triggers": {
            "positive": ["工作成就", "社交互动", "运动"],
            "negative": ["工作压力", "睡眠不足"]
        }
    },
    "social_insights": {
        "network_growth": [100, 105, 110, 115, 120],
        "interaction_quality": {
            "chat": 0.85,
            "meetup": 0.9,
            "online": 0.8
        },
        "relationship_strength": {
            "close_friends": 5,
            "regular_contacts": 15,
            "acquaintances": 100
        }
    },
    "behavior_insights": {
        "activity_patterns": {
            "morning": ["工作", "运动"],
            "afternoon": ["会议", "社交"],
            "evening": ["休闲", "学习"]
        },
        "productivity_metrics": {
            "focus_time": 6.5,
            "breaks": 4,
            "distractions": 2
        }
    },
    "risk_insights": {
        "alert_history": [
            {
                "date": "2024-03-15",
                "type": "stress",
                "level": "medium",
                "resolved": true
            }
        ],
        "risk_trends": {
            "stress": "decreasing",
            "anxiety": "stable",
            "depression": "low"
        }
    },
    "recommendations": {
        "short_term": [
            "增加户外活动时间",
            "保持规律的作息"
        ],
        "long_term": [
            "培养新的兴趣爱好",
            "建立更广泛的社交网络"
        ]
    },
    "generated_at": "2024-03-31T10:00:00"
}
```

### 预测用户情绪状态
```http
POST /api/v1/profile/predict-emotion
Authorization: Bearer your_token
Content-Type: application/json

{
    "user_id": "user_123",
    "context": {
        "time_of_day": 0.5,
        "day_of_week": 1,
        "weather_score": 0.8,
        "recent_activities": ["work", "exercise"],
        "social_interactions": 3,
        "sleep_quality": 0.9
    }
}
```

响应：
```json
{
    "user_id": "user_123",
    "predicted_emotion": "positive",
    "confidence": 0.85,
    "factors": {
        "positive": [
            {
                "factor": "recent_activities",
                "impact": 0.3,
                "details": "今天完成了重要工作并进行了运动"
            },
            {
                "factor": "social_interactions",
                "impact": 0.2,
                "details": "有3次积极的社交互动"
            }
        ],
        "negative": [
            {
                "factor": "time_of_day",
                "impact": 0.1,
                "details": "下午可能有些疲劳"
            }
        ]
    },
    "recommendations": [
        "可以适当休息一下",
        "建议与同事交流工作进展"
    ],
    "predicted_at": "2024-03-31T10:00:00"
}
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

## 社交情绪

### 记录社交互动
```http
POST /api/v1/social/interactions
Authorization: Bearer your_token
Content-Type: application/json

{
    "user_id": "user_123",
    "interaction_type": "chat",
    "emotion_type": "positive",
    "intensity": 0.8,
    "context": "与朋友聊天",
    "timestamp": "2024-03-31T10:00:00",
    "interaction_id": "interaction_456",
    "target_user_id": "user_789"
}
```

响应：
```json
{
    "id": "record_123",
    "user_id": "user_123",
    "interaction_type": "chat",
    "emotion_type": "positive",
    "intensity": 0.8,
    "context": "与朋友聊天",
    "timestamp": "2024-03-31T10:00:00",
    "interaction_id": "interaction_456",
    "target_user_id": "user_789"
}
```

### 获取社交情绪分析
```http
GET /api/v1/social/analysis/{user_id}
Authorization: Bearer your_token
```

响应：
```json
{
    "user_id": "user_123",
    "social_emotion_score": 0.75,
    "social_engagement": 0.85,
    "social_network_size": 100,
    "interaction_patterns": {
        "chat": 0.4,
        "comment": 0.2,
        "like": 0.2,
        "share": 0.1,
        "follow": 0.1
    },
    "emotional_contagion": 0.65
}
```

### 获取社交情绪趋势
```http
GET /api/v1/social/trend/{user_id}
Authorization: Bearer your_token
Query Parameters:
- time_period: 时间周期（可选值：day, week, month, year）
```

响应：
```json
{
    "user_id": "user_123",
    "time_period": "week",
    "emotion_scores": [0.8, 0.7, 0.85, 0.75, 0.9, 0.8, 0.85],
    "engagement_scores": [0.9, 0.85, 0.95, 0.9, 0.85, 0.9, 0.95],
    "network_growth": [100, 102, 105, 108, 110, 112, 115],
    "interaction_counts": {
        "chat": [10, 12, 8, 15, 11, 13, 9],
        "comment": [5, 6, 4, 7, 5, 6, 4],
        "like": [20, 25, 18, 22, 24, 20, 23]
    },
    "timestamps": [
        "2024-03-25T00:00:00",
        "2024-03-26T00:00:00",
        "2024-03-27T00:00:00",
        "2024-03-28T00:00:00",
        "2024-03-29T00:00:00",
        "2024-03-30T00:00:00",
        "2024-03-31T00:00:00"
    ]
}
```

### 获取社交情绪洞察
```http
GET /api/v1/social/insights/{user_id}
Authorization: Bearer your_token
```

响应：
```json
{
    "user_id": "user_123",
    "top_interactions": [
        {
            "type": "chat",
            "frequency": 0.4,
            "emotional_impact": 0.85
        },
        {
            "type": "comment",
            "frequency": 0.2,
            "emotional_impact": 0.75
        }
    ],
    "emotional_impact": {
        "chat": 0.85,
        "comment": 0.75,
        "like": 0.6,
        "share": 0.8,
        "follow": 0.7
    },
    "social_support": 0.85,
    "social_stress": 0.2,
    "relationship_quality": {
        "family": 0.9,
        "friends": 0.85,
        "colleagues": 0.75,
        "acquaintances": 0.6
    }
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