
import sys
import os
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from src.config import settings
from src.services.rag_service import RAGService
from src.services.chat_service import ChatService
from src.models.chat_session import Base

# Setup DB
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_rag_service():
    print("--- Testing RAG Service ---")
    try:
        rag = RAGService()
        print(f"RAG Service initialized. Model: {rag.model_name}")
        
        # Test basic search (mock or real)
        print("Running search...")
        results = rag.search_embeddings("humanoid robot", top_k=1)
        print(f"Search results: {len(results)}")
        if results:
            print(f"First result: {results[0].content[:50]}...")
            
        # Test generation (if API key present)
        if settings.groq_api_key:
            print("Running generation...")
            answer = rag.generate_answer("What is a humanoid?", results)
            print(f"Answer: {answer[:100]}...")
        else:
            print("Skipping generation (no GROQ_API_KEY)")
            
    except Exception as e:
        print(f"RAG Service Failed: {e}")
        import traceback
        traceback.print_exc()

def test_db_service():
    print("\n--- Testing Chat Service (DB) ---")
    try:
        chat = ChatService()
        db = SessionLocal()
        
        # Create session
        print("Creating session...")
        session = chat.create_session(db)
        print(f"Session created: {session.id}")
        
        # Add message
        print("Adding message...")
        msg = chat.create_message(db, session.id, "user", "Hello")
        print(f"Message added: {msg.id}")
        
        db.close()
        print("DB Service OK")
    except Exception as e:
        print(f"DB Service Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rag_service()
    test_db_service()
