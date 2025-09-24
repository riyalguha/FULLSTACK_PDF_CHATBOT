# ui.py
import streamlit as st
import requests

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/ask" # URL of your FastAPI backend

# --- Streamlit App UI ---
st.set_page_config(page_title="DocBot", layout="wide")
st.title("📄 DocBot: Chat with Your Documents")

st.info("This is a demo of a Retrieval-Augmented Generation (RAG) chatbot. Ask a question about your document below.")

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your document..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Call the FastAPI backend
            response = requests.post(API_URL, json={"query": prompt})
            response.raise_for_status() # Raise an exception for bad status codes
            
            result = response.json()
            answer = result.get("answer", "Sorry, I couldn't find an answer.")
            sources = result.get("sources", "No sources available.")
            
            # --- Pro-Level Feature: Displaying Sources ---
            full_response = f"{answer}\n\n---\n*Sources:*\n{sources}"
            
            message_placeholder.markdown(full_response)
        
        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend: {e}")
            full_response = "Error: Could not connect to the backend."

    st.session_state.messages.append({"role": "assistant", "content": full_response})