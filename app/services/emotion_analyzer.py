from transformers import pipeline
from app.core.config import settings
import torch

class EmotionAnalyzer:
    def __init__(self):
        self.model = pipeline(
            "sentiment-analysis",
            model=settings.MODEL_NAME,
            device=0 if torch.cuda.is_available() else -1
        )
        
        # 情绪标签映射
        self.emotion_mapping = {
            "positive": ["快乐", "满足", "兴奋", "期待"],
            "negative": ["悲伤", "焦虑", "愤怒", "失望"],
            "neutral": ["平静", "思考", "专注", "放松"]
        }
    
    async def analyze_text(self, text: str):
        """
        分析文本情感
        """
        try:
            # 使用模型进行情感分析
            result = self.model(text, max_length=settings.MAX_LENGTH)
            
            # 处理结果
            score = float(result[0]["score"])
            label = result[0]["label"]
            
            # 根据得分确定情绪
            if score > 0.6:
                emotion = "positive"
            elif score < 0.4:
                emotion = "negative"
            else:
                emotion = "neutral"
            
            return {
                "text": text,
                "score": score,
                "emotion": emotion,
                "confidence": score,
                "details": {
                    "label": label,
                    "possible_emotions": self.emotion_mapping[emotion]
                }
            }
            
        except Exception as e:
            raise Exception(f"情感分析失败: {str(e)}")
    
    async def generate_suggestions(self, emotion: str, score: float):
        """
        根据情绪生成建议
        """
        suggestions = []
        
        if emotion == "negative":
            if score < 0.3:
                suggestions.extend([
                    "建议进行深呼吸练习",
                    "可以尝试与朋友倾诉",
                    "适当运动可以帮助改善心情"
                ])
            else:
                suggestions.extend([
                    "听听舒缓的音乐",
                    "尝试写写日记",
                    "做一些让自己开心的事情"
                ])
        elif emotion == "neutral":
            suggestions.extend([
                "保持当前的状态",
                "可以尝试新的活动",
                "记录下此刻的感受"
            ])
        else:
            suggestions.extend([
                "继续保持积极的心态",
                "分享你的快乐给他人",
                "记录下让你开心的事情"
            ])
        
        return suggestions 