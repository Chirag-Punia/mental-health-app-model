from .knowledge_base import KnowledgeBase
from .emotion_analysis import EmotionAnalyzer
from .rag_pipeline import RAGPipeline
from .safety_mechanisms import SafetyMechanisms
import argparse

def main():
    # Initialize components
    kb = KnowledgeBase()
    emotion_analyzer = EmotionAnalyzer()
    rag = RAGPipeline()
    safety = SafetyMechanisms()
    
    # Chat interface
    print("Mental Health Assistant - Type 'exit' to quit.")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        
        # Emotion analysis
        emotion = emotion_analyzer.analyze_text(query)
        print(f"[Detected Emotion: {emotion['emotion']} ({emotion['confidence']:.2f})]")
        
        # Crisis detection
        if safety.detect_crisis(query):
            print(safety.handle_crisis())
            continue
        
        # Query existing Pinecone index
        context = kb.query_index(query)
        if context:
            response = rag.generate_response(query, "\n".join(context))
            print(f"Assistant: {response}\n")
        else:
            print("Assistant: I couldn't find relevant information. Please try rephrasing your query.\n")

if __name__ == "__main__":
    main()