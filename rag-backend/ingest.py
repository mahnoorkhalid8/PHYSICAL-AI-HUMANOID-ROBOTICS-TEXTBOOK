
import os
from qdrant_client import QdrantClient, models
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "humanoid_robotics_textbook")
DOCS_PATH = os.getenv("DOCS_PATH", "humanoid-robotics/docs")

class Ingester:
    def __init__(self):
        self.qdrant_client = QdrantClient(host=QDRANT_HOST, api_key=QDRANT_API_KEY)
        self.embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def _load_mdx_files(self, directory):
        """Loads all .mdx files from the specified directory."""
        mdx_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".mdx"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        mdx_files.append({"content": content, "source": file_path})
        return mdx_files

    def ingest_data(self):
        """Ingests MDX data into Qdrant."""
        print(f"Loading MDX files from {DOCS_PATH}...")
        mdx_data = self._load_mdx_files(DOCS_PATH)
        print(f"Found {len(mdx_data)} MDX files.")

        if not mdx_data:
            print("No MDX files found to ingest.")
            return

        # Prepare points for Qdrant
        points = []
        for doc in mdx_data:
            chunks = self.text_splitter.split_text(doc["content"])
            for i, chunk in enumerate(chunks):
                # Ensure text is not empty before embedding
                if chunk.strip():
                    embedding = self.embeddings_model.embed_query(chunk)
                    points.append(
                        models.PointStruct(
                            id=f"{doc['source']}-{i}",
                            payload={"content": chunk, "source": doc["source"]},
                            vector=embedding,
                        )
                    )
                else:
                    print(f"Skipping empty chunk from {doc['source']} index {i}")

        if not points:
            print("No valid chunks generated for ingestion.")
            return

        # Create collection if it doesn't exist
        print(f"Ensuring Qdrant collection '{QDRANT_COLLECTION_NAME}' exists...")
        self.qdrant_client.recreate_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=len(points[0].vector), distance=models.Distance.COSINE),
        )

        # Upload data to Qdrant
        print(f"Uploading {len(points)} points to Qdrant...")
        self.qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            wait=True,
            points=points
        )
        print("Data ingestion complete.")

if __name__ == "__main__":
    ingester = Ingester()
    ingester.ingest_data()
