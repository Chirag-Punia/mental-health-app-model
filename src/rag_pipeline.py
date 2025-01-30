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
        """Generate a response using Gemini."""
        prompt = f"""
        You are a compassionate and supportive mental health assistant, designed to provide encouragement, empathy, and guidance. 
        
        **User Query:**  
        {query}
        
        **Context (Background Information):**  
        {context}

        **Guidelines for Your Response:**  
        - Be **empathetic, understanding, and non-judgmental**.  
        - Use **reassuring and supportive** language.  
        - **Acknowledge** the user's emotions and validate their feelings.  
        - **Encourage self-care** and positive coping mechanisms.  
        - **Do not provide medical advice** or diagnose conditions.  
        - If the user requires professional help, gently **suggest seeking a licensed therapist**.  
        - If unsure or the topic is beyond your expertise, respond with:  
        *"I'm here to support you, but I’m not qualified to provide medical advice. I recommend speaking with a mental health professional."*
        
        **Example Response Style:**  
        - "I hear you. That sounds really challenging, and I want you to know you're not alone."  
        - "It's completely understandable to feel this way. Taking small steps, like talking to someone you trust, can be really helpful."  
        - "If this is overwhelming, reaching out to a therapist could be a great step. You're doing the right thing by seeking support."  

        Now, respond thoughtfully based on the query and context.
        """
        return genai.GenerativeModel('gemini-pro').generate_content(prompt).text