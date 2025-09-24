# download_model.py
from langchain_huggingface import HuggingFaceEmbeddings
import os

def download_model():
    """
    Downloads the embedding model from Hugging Face and saves it to a local directory.
    """
    model_name = "all-MiniLM-L6-v2"
    # We will save the model to a directory named "models"
    model_path = os.path.join(os.getcwd(), "models")
    
    print(f"Downloading model to {model_path}...")
    
    # Use cache_folder to specify the download directory
    HuggingFaceEmbeddings(model_name=model_name, cache_folder=model_path)
    
    print("Model downloaded successfully.")

if __name__ == '__main__':
    download_model()# download_model.py
from langchain_huggingface import HuggingFaceEmbeddings
import os

def download_model():
    """
    Downloads the embedding model from Hugging Face and saves it to a local directory.
    """
    model_name = "all-MiniLM-L6-v2"
    # We will save the model to a directory named "models"
    model_path = os.path.join(os.getcwd(), "models")
    
    print(f"Downloading model to {model_path}...")
    
    # Use cache_folder to specify the download directory
    HuggingFaceEmbeddings(model_name=model_name, cache_folder=model_path)
    
    print("Model downloaded successfully.")

if __name__ == '__main__':
    download_model()