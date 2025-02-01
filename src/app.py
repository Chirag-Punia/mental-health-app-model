from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .knowledge_base import KnowledgeBase
from .emotion_analysis import EmotionAnalyzer
from .rag_pipeline import RAGPipeline
from .safety_mechanisms import SafetyMechanisms
import os
import uuid

app = FastAPI()

# Initialize components
kb = KnowledgeBase()
emotion_analyzer = EmotionAnalyzer()
rag = RAGPipeline()
safety = SafetyMechanisms()

# Session storage (in-memory, replace with a database for production)
sessions: dict[str, list[str]] = {}

class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None  # Optional session ID

class ChatResponse(BaseModel):
    response: str
    emotion: dict
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    query = request.query
    session_id = request.session_id

    # If no session ID is provided or it's invalid, create a new one
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = []

    # Add user input to session history
    sessions[session_id].append(f"User: {query}")

    # Emotion analysis
    emotion = emotion_analyzer.analyze_text(query)

    # Crisis detection
    if safety.detect_crisis(query):
        response = safety.handle_crisis()
        sessions[session_id].append(f"Assistant: {response}")
        return ChatResponse(response=response, emotion=emotion, session_id=session_id)

    # Check if user is asking for conversation history
    if "remember" in query.lower() or "what was my last input" in query.lower():
        if len(sessions[session_id]) > 1:
            last_input = sessions[session_id][-2].replace("User: ", "")  # Get last user message
            response = f"Your last input was: '{last_input}'."
        else:
            response = "This is the start of our conversation."
        sessions[session_id].append(f"Assistant: {response}")
        return ChatResponse(response=response, emotion=emotion, session_id=session_id)
    
    # Retrieve context from Pinecone
    context = kb.query_index(query)
    if not context:
        response = "I couldn't find relevant information. Can you provide more details?"
        sessions[session_id].append(f"Assistant: {response}")
        return ChatResponse(response=response, emotion=emotion, session_id=session_id)

    # Include conversation history in context
    conversation_history = "\n".join(sessions[session_id][-10:])  # Keep only last 10 messages
    full_context = f"Conversation History:\n{conversation_history}\n\nRelevant Context:\n{context}"

    # Generate response
    response = rag.generate_response(query, full_context)
    sessions[session_id].append(f"Assistant: {response}")

    return ChatResponse(response=response, emotion=emotion, session_id=session_id)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
