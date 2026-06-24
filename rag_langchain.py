import os 
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

PDF_PATH = "data/Black and White Simple Business School Graduate Corporate Resume.pdf"
print("Loading and splitting the pdf.....")

loader = PyPDFLoader(PDF_PATH)

docs = loader.load()

text_spliter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 100)
splits = text_spliter.split_text(docs)

print("Building the vector store")
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("API_KEY")
)
vectorStore = FAISS.from_documents(splits,embeddings)
retriver = vectorStore.as_retriever(search_kwargs = {"k" : 10})

llm = ChatGoogleGenerativeAI(api_key = os.getenv("API_KEY"),model="gemini-2.5-flash")

system_prompt = (
    "you are a resume analyzer",
    "The context below is extracted from a resume",
    "Answer the question only based in retrived data, do not make aaumptions",
    "if the information not found just say not found",
    "{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    ("user",{input})
])