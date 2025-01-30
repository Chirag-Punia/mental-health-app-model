from .config import Config

config = Config()

class SafetyMechanisms:
    def __init__(self):
        self.crisis_keywords = config.safety_keywords
    
    def detect_crisis(self, query: str) -> bool:
        """Check if the query indicates a crisis."""
        return any(keyword in query.lower() for keyword in self.crisis_keywords)
    
    def handle_crisis(self) -> str:
        """Provide crisis resources."""
        return config.crisis_resources