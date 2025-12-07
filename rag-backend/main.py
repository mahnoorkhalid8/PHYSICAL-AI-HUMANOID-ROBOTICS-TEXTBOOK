
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient, models
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "humanoid_robotics_textbook")

class ChatRequest(BaseModel):
    query: str
    selected_text: str | None = None

@app.on_event("startup")
async def startup_event():
    global qdrant_client, embeddings_model, llm, qa_chain
    try:
        qdrant_client = QdrantClient(host=QDRANT_HOST, api_key=QDRANT_API_KEY)
        embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0)

        # Create a retriever from Qdrant
        qdrant_retriever = qdrant_client.as_retriever(
            collection_name=QDRANT_COLLECTION_NAME,
            embeddings=embeddings_model,
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=qdrant_retriever,
            return_source_documents=True
        )
        print("FastAPI startup: Qdrant client, embeddings, and QA chain initialized.")
    except Exception as e:
        print(f"FastAPI startup error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to initialize RAG components: {e}")

@app.get("/")
async def read_root():
    return {"message": "RAG Backend is running"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Combine query and selected_text if available
        full_query = request.query
        if request.selected_text:
            full_query = f"Context: {request.selected_text}\n\nQuestion: {request.query}"

        result = qa_chain({"query": full_query})
        response = result["result"]
        source_documents = result.get("source_documents", [])

        source_urls = list(set([doc.metadata.get("source") for doc in source_documents if doc.metadata.get("source")]))

        return {"response": response, "source_urls": source_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
