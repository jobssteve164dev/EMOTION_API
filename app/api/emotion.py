from fastapi import APIRouter, HTTPException
from app.models.emotion import EmotionAnalysis, EmotionResponse
from app.services.emotion_analyzer import EmotionAnalyzer
from typing import List

router = APIRouter()
emotion_analyzer = EmotionAnalyzer()

@router.post("/analyze", response_model=EmotionResponse)
async def analyze_emotion(text: str):
    """
    分析文本情感
    """
    try:
        # 进行情感分析
        analysis = await emotion_analyzer.analyze_text(text)
        
        # 生成建议
        suggestions = await emotion_analyzer.generate_suggestions(
            analysis["emotion"],
            analysis["score"]
        )
        
        return EmotionResponse(
            analysis=EmotionAnalysis(**analysis),
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """
    检查服务健康状态
    """
    return {
        "status": "healthy",
        "model": "loaded",
        "service": "emotion_analysis"
    } 