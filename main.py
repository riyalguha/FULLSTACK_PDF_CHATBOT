# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
DB_DIRECTORY = "db"
# EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- FastAPI App Initialization ---
app = FastAPI(
    title="RAG Chatbot API",
    description="An API for chatting with your documents.",
    version="1.0.0"
)

# --- Pydantic Models for Request/Response ---
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: str # For citing sources

# --- Load the necessary components ---
embeddings = HuggingFaceEmbeddings(model_name="./models")
vectordb = Chroma(persist_directory=DB_DIRECTORY, embedding_function=embeddings)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1, convert_system_message_to_human=True)
retriever = vectordb.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 chunks

prompt_template = """
Use the following context to answer the user's question.
If you don't know the answer, just say you don't know. DON'T try to make up an answer.
Provide a detailed and helpful answer based on the context.

Context: {context}
Question: {question}

Helpful Answer:
"""
QA_PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_PROMPT}
)

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """
    Receives a query and returns the answer and sources from the RAG pipeline.
    """
    result = qa_chain({"query": request.query})
    
    answer = result.get("result", "No answer found.")
    
    # --- Pro-Level Feature: Citing Sources ---
    source_documents = result.get("source_documents", [])
    if source_documents:
        sources = "\n".join([doc.metadata.get('source', 'Unknown') for doc in source_documents])
    else:
        sources = "No sources found."
        
    return QueryResponse(answer=answer, sources=sources)