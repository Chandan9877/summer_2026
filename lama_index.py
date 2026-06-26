import os
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, Settings
from llama_index.readers.file import PyMuPDFReader
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

load_dotenv()

loader = PyMuPDFReader()

docs = loader.load_data(file_path="Tutorial%2014%20Unit%205.pdf")

Settings.llm = GoogleGenAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("API_KEY")
)

Settings.embed_model = GoogleGenAIEmbedding(
    model_name="models/embedding-001",
    api_key=os.getenv("API_KEY")
)

index = VectorStoreIndex.from_documents(docs)

query_engine = index.as_query_engine()

response = query_engine.query("Summarize this document")

print(response)