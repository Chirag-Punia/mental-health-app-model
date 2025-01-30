from transformers import pipeline
from .config import Config

config = Config()

class EmotionAnalyzer:
    def __init__(self):
        # Use a non-TensorFlow model to avoid Keras conflicts
        self.model = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            framework="pt"  # Use PyTorch instead of TensorFlow
        )
    
    def analyze_text(self, text: str) -> dict:
        """Detect emotions from text input."""
        result = self.model(text)[0]
        return {
            "emotion": result["label"],
            "confidence": result["score"]
        }