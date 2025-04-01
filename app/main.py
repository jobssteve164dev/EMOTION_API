from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, emotion, user_profile, user_behavior, alert, social_emotion
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    情感分析引擎 API 服务
    
    提供以下功能：
    * 用户认证和授权
    * 文本情感分析
    * 情绪追踪
    * 心理状态评估
    * 用户画像分析
    * 用户行为分析
    * 个性化推荐
    * 社交情绪分析
    * 情绪预警系统
    
    使用说明：
    1. 首先通过 /api/v1/token 获取访问令牌
    2. 在后续请求中使用 Bearer Token 进行认证
    * 所有情感分析相关的API都需要认证
    """,
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(emotion.router, prefix="/api/v1/emotion", tags=["情绪分析"])
app.include_router(user_profile.router, prefix="/api/v1/profile", tags=["用户画像"])
app.include_router(user_behavior.router, prefix="/api/v1/behavior", tags=["用户行为"])
app.include_router(alert.router, prefix="/api/v1/alert", tags=["情绪预警"])
app.include_router(social_emotion.router, prefix="/api/v1/social", tags=["社交情绪"])

@app.get("/")
async def root():
    return {
        "message": "欢迎使用情感分析引擎API",
        "version": settings.VERSION,
        "docs_url": "/api/docs",
        "redoc_url": "/api/redoc"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "emotion_analysis": "available",
            "database": "available",
            "authentication": "available",
            "user_profile": "available",
            "user_behavior": "available",
            "alert_system": "available",
            "social_emotion": "available"
        }
    } 