# 情感分析引擎 SDK

这是一个用于调用情感分析引擎API的Python SDK。

## 安装

```bash
pip install emotion-sdk
```

## 快速开始

```python
from emotion_sdk import EmotionSDK

# 初始化SDK
sdk = EmotionSDK("http://localhost:8000")

# 登录
sdk.login("your_username", "your_password")

# 分析文本情感
result = sdk.analyze_emotion("今天天气真好，我很开心！")
print(result)

# 获取用户情感历史
history = sdk.get_emotion_history("user_id")
print(history)

# 获取情感趋势
trend = sdk.get_emotion_trend("user_id", days=30)
print(trend)

# 关闭连接
sdk.close()
```

## API 文档

### EmotionSDK

#### 初始化

```python
sdk = EmotionSDK(base_url: str, api_key: Optional[str] = None)
```

参数：
- `base_url`: API服务器地址
- `api_key`: API密钥（可选）

#### 登录

```python
sdk.login(username: str, password: str) -> bool
```

参数：
- `username`: 用户名
- `password`: 密码

返回：
- `bool`: 登录是否成功

#### 情感分析

```python
sdk.analyze_emotion(text: str) -> Dict
```

参数：
- `text`: 待分析文本

返回：
- `Dict`: 分析结果，包含情感得分、情绪类型等信息

#### 获取情感历史

```python
sdk.get_emotion_history(
    user_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Dict]
```

参数：
- `user_id`: 用户ID
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）

返回：
- `List[Dict]`: 历史记录列表

#### 获取情感趋势

```python
sdk.get_emotion_trend(user_id: str, days: int = 30) -> Dict
```

参数：
- `user_id`: 用户ID
- `days`: 统计天数

返回：
- `Dict`: 趋势数据

## 错误处理

SDK会抛出以下异常：

- `requests.exceptions.RequestException`: 网络请求错误
- `ValueError`: 参数错误
- `Exception`: 其他错误

示例：
```python
try:
    result = sdk.analyze_emotion("测试文本")
except requests.exceptions.RequestException as e:
    print(f"网络错误: {e}")
except ValueError as e:
    print(f"参数错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 最佳实践

1. **连接管理**
   ```python
   # 使用上下文管理器
   with EmotionSDK("http://localhost:8000") as sdk:
       result = sdk.analyze_emotion("测试文本")
   ```

2. **错误重试**
   ```python
   from requests.adapters import HTTPAdapter
   from requests.packages.urllib3.util.retry import Retry

   sdk = EmotionSDK("http://localhost:8000")
   retry = Retry(total=3, backoff_factor=0.1)
   sdk.session.mount('http://', HTTPAdapter(max_retries=retry))
   ```

3. **异步调用**
   ```python
   import asyncio
   from concurrent.futures import ThreadPoolExecutor

   async def analyze_batch(texts):
       with EmotionSDK("http://localhost:8000") as sdk:
           with ThreadPoolExecutor() as executor:
               tasks = [
                   asyncio.get_event_loop().run_in_executor(
                       executor, sdk.analyze_emotion, text
                   )
                   for text in texts
               ]
               return await asyncio.gather(*tasks)
   ```

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的情感分析功能
- 支持用户认证
- 支持历史记录查询
- 支持趋势分析 