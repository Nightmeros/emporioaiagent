import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GOOGLE_API_KEY")

def setup_rag():
    pdf_path = os.path.join(base_dir, "data", "arquivos", "políticas_da_loja.pdf")
    chroma_dir = os.path.join(base_dir, "data", "database", "chroma_db")

    loader = PyPDFLoader(pdf_path)
    documentos = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    blocos = text_splitter.split_documents(documentos)
    
    print(f"🧠 A gerar embeddings para {len(blocos)} blocos e a criar a base vetorial...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
    )
    vectorstore = Chroma.from_documents(
        documents=blocos,
        embedding=embeddings,
        persist_directory=chroma_dir
    )
    
    print(f"✅ Base vetorial RAG criada com sucesso em: {chroma_dir}")

if __name__ == "__main__":
    setup_rag()