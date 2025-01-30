import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.pinecone_api = os.getenv("PINECONE_API")
        self.gemini_api = os.getenv("GEMINI_API")
        self.serpapi_api = os.getenv("SERPAPI_API")
        self.index_name = "medicalbot"  # Your Pinecone index name
        self.embedding_dim = 384  # Dimension for embeddings
        self.safety_keywords = ["suicide", "self-harm", "kill myself", "abuse"]
        self.crisis_resources = """
        If you're in crisis, please contact:
        - National Suicide Prevention Lifeline: 988 (US)
        - Crisis Text Line: Text HOME to 741741 (US)
        - Your local emergency services
        """