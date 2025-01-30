from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .knowledge_base import KnowledgeBase
from .emotion_analysis import EmotionAnalyzer
from .rag_pipeline import RAGPipeline
from .safety_mechanisms import SafetyMechanisms
import os

app = FastAPI()

# Initialize components
kb = KnowledgeBase()
emotion_analyzer = EmotionAnalyzer()
rag = RAGPipeline()
safety = SafetyMechanisms()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    emotion: dict

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    query = request.query
    
    # Emotion analysis
    emotion = emotion_analyzer.analyze_text(query)
    
    # Crisis detection
    if safety.detect_crisis(query):
        return ChatResponse(
            response=safety.handle_crisis(),
            emotion=emotion
        )
    
    # Query Pinecone index
    context = kb.query_index(query)
    if not context:
        return ChatResponse(
            response="I couldn't find relevant information. Please try rephrasing your query.",
            emotion=emotion
        )
    
    # Generate response
    response = rag.generate_response(query, "\n".join(context))
    return ChatResponse(response=response, emotion=emotion)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}