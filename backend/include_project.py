"""
There are multiple ways to access an entire project. We chose Retrieval Augmented Generation (RAG) for the following reasons:

1. RAG allows us to access the specific files we want to create tests for, instead of the whole project as context. This enables us to stay within all necessary character limits for queries.
2. The database can be modified easily, which is necessary for creating tests for continually changing code in development.

-----------------

RAG works like this:

Fill database:
The project is uploaded into an external database with the use of embeddings. 
The data is separated into chunks and then sent to an embedding model. 
This generates a vector location for each chunk and stores it in a vector database. 

Prompt:
Each user prompt is also sent to a RAG retriever. 
This RAG retriever takes the prompt and sends it to the same embedding model, which performs a similarity search and returns the most relevant chunks that are likely to have the information necessary for the user's prompt. 
The information from these chunks can now be put into the context window of the LLM. 
"""
import argparse
import os
import shutil
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader, PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from llm_manager import LLMManager

DATA_PATH = "python-test-cases"
CHROMA_PATH = "chroma"

def main():
    db = None  # Ensure db is always defined
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    parser.add_argument(
        "--model",
        type=int,
        default=0,
        help="Model selection index (default: 0)",
    )
    args = parser.parse_args()

    # Load allowed models and select model_id
    config = load_allowed_models_config()
    loaded_models = config.get("models", [])
    if not loaded_models:
        raise ValueError("No models found in allowed_models.json")
    model = loaded_models[args.model]
    model_id = model["id"]

    manager = LLMManager()
    try:
        manager.start_model_container(model_id)
        if args.reset:
            print("✨ Clearing Database")
            clear_database()

        # Create (or update) the data store.
        documents = load_documents()
        chunks = split_documents(documents)
        db = add_to_chroma(chunks)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise
    finally:
        # Cleanup resources
        print("\n🧹 Cleaning up...")
        if db and hasattr(db, 'close'):
            db.close()
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
        manager.stop_model_container(model_id)
        print("✅ Cleanup complete")

# Populate database

def load_documents():
    # Opens the Python files in the directory
    document_loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.py",
        loader_cls=PythonLoader
    )
    return document_loader.load()

def split_documents(documents: list[Document]):
    # Splits documents into smaller chunks to fit in the context window
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


# Create embeddings to populate database and query
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_MODELS = "allowed_models.json"

def load_allowed_models_config():
    config_path = os.path.join(SCRIPT_DIR, ALLOWED_MODELS)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_embedding_function():
    # Other open-source embeddings can be used to enhance performance, if necessary
    # https://python.langchain.com/docs/integrations/text_embedding/
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate chunk IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    db.persist()
    return db

def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page metadata.
        chunk.metadata["id"] = chunk_id

    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()


# Still open: Add a function to update the chunk when a file is edited
# A section of this code is inspired by https://github.com/pixegami/rag-tutorial-v2
