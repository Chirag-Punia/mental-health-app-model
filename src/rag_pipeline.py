import google.generativeai as genai
from serpapi import GoogleSearch
import pinecone
from .config import Config

config = Config()
genai.configure(api_key=config.gemini_api)

class RAGPipeline:
    def __init__(self):
        # Initialize Pinecone client
        self.pc = pinecone.Pinecone(api_key=config.pinecone_api)
        self.index = self.pc.Index(config.index_name)

    def retrieve_context(self, query: str) -> str:
        """Retrieve context from Pinecone or web search."""
        # Step 1: Search Pinecone
        query_embed = genai.embed_content(
            model="models/embedding-001",
            content=query,
            task_type="RETRIEVAL_QUERY"
        )['embedding']
        
        results = self.index.query(vector=query_embed, top_k=3, include_metadata=True)
        if results["matches"][0]["score"] > 0.7:
            return "\n".join([match["metadata"]["text"] for match in results["matches"]])
        
        # Step 2: Fallback to web search
        return self._web_search(query)
    
    def _web_search(self, query: str) -> str:
        """Perform a web search using SerpAPI."""
        params = {
            "q": query,
            "api_key": config.serpapi_api,
            "engine": "google",
            "num": 3
        }
        results = GoogleSearch(params).get_dict()
        return "\n".join([r.get("snippet", "") for r in results.get("organic_results", [])])
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate a response using Gemini, including conversation history and helpful advice."""
        prompt = f"""
        You are a mental health assistant. Respond to this query:
        {query}
        
        Context:
        {context}
        
        Rules:
        - Be empathetic and supportive.
        - Provide practical self-help strategies and general tips when possible.
        - Recommend seeking professional help only if the situation seems severe or unmanageable.
        - Never give medical advice.
        - If unsure, say "I'm not qualified to answer that."
        - Maintain context from previous messages in the conversation.
        
        Format:
        - Start with an empathetic acknowledgment.
        - Offer general self-help techniques (e.g., breathing exercises, journaling, mindfulness).
        - If the issue seems severe, suggest seeking professional help in a compassionate manner.
        """

        return genai.GenerativeModel('gemini-pro').generate_content(prompt).text
