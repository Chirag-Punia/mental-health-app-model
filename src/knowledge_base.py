import pinecone
import google.generativeai as genai
from .config import Config
from sentence_transformers import SentenceTransformer

config = Config()
genai.configure(api_key=config.gemini_api)

class KnowledgeBase:
    def __init__(self):
        # Initialize Pinecone client
        self.pc = pinecone.Pinecone(api_key=config.pinecone_api)
        self.index = self.pc.Index(config.index_name)

        # Load model once (lighter alternative)
        self.embedding_model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2", device="cpu")
        self.embedding_model.half()  # Reduce memory usage with FP16 precision

    def query_index(self, query: str, top_k: int = 3) -> list:
        """Query the existing Pinecone index for relevant context."""
        # Generate query embedding
        query_embed = self.embedding_model.encode(query).tolist()  # 384-dim vector
        
        # Query Pinecone
        results = self.index.query(
            vector=query_embed,
            top_k=top_k,
            include_metadata=True
        )
        
        # Return relevant context
        return [match["metadata"]["text"] for match in results["matches"]]
