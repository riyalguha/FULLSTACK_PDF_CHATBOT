import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
PDF_PATH = "data/Resume.pdf" # Make a data folder and put your PDF there
DB_DIRECTORY = "db"
# EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

def main():
    print("Starting data ingestion process...")

    # 1. Load the document
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    if not documents:
        print("Could not load any documents. Check the PDF path.")
        return
    print(f"Loaded {len(documents)} document(s).")

    # 2. Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)
    print(f"Split document into {len(texts)} chunks.")

    # 3. Create embeddings
    # This will download the model from Hugging Face and run it locally
    embeddings = HuggingFaceEmbeddings(model_name="./models")
    print("Embedding model loaded.")

    # 4. Store chunks in ChromaDB
    # This will create a persistent database in the 'db' directory
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=DB_DIRECTORY
    )
    # vectordb.persist()
    print(f"Successfully created and persisted vector database at {DB_DIRECTORY}")

if __name__ == "__main__":
    main()