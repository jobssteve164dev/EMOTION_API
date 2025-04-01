# 情感分析引擎

一个强大的情感分析引擎，提供情绪分析、用户画像、行为分析和情绪预警等功能。

## 功能特点

- 文本情感分析
- 用户情绪追踪
- 用户画像构建
- 用户行为分析
- 情绪预警系统
- 个性化推荐

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

## 快速开始

### 安装

```bash
pip install emotion-sdk
```

### 使用示例

```python
from emotion_sdk import EmotionSDK

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

# 获取预警历史
alerts = sdk.get_alert_history()
print(f"当前活动预警数: {alerts['active_alerts']}")

# 关闭连接
sdk.close()
```

## API文档

详细的API文档请参考 [API文档](docs/API.md)

## SDK文档

详细的SDK使用说明请参考 [SDK文档](docs/SDK.md)

## 开发环境设置

1. 克隆仓库
```bash
git clone https://github.com/your-username/emotion-api.git
cd emotion-api
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

5. 运行开发服务器
```bash
uvicorn app.main:app --reload
```

## 测试

运行测试：
```bash
pytest
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目维护者：[Your Name](mailto:your.email@example.com)
- 项目主页：[GitHub](https://github.com/your-username/emotion-api) 