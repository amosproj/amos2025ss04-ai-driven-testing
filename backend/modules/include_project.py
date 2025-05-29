from modules.base import ModuleBase
import os
import shutil
import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from llm_manager import LLMManager
import subprocess

CHROMA_PATH = "chroma"
ALLOWED_MODELS = "allowed_models.json"
GITHUB_REPO_URL = "https://github.com/phiho1609/derOrtAnDemIDahoamBims"
CLONE_PATH = Path(__file__).parent.parent / "cloned_project"
LOCAL_PATH = Path(__file__).parent.parent / "../python-test-cases"
PROMPT_TEMPLATE = """
Answer the query based only on the following context:
{context}
---
Answer the query based on the above context: {question}
"""


class IncludeProject(ModuleBase):
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return False

    def process_prompt(self, prompt_data: dict) -> dict:
        # Expect prompt_data to contain 'model_index', 'reset', and 'prompt' keys

        db = None  # Ensure db is always defined

        # Load allowed models and select model_id
        model_index = prompt_data.get("model_index", 0)
        reset = prompt_data.get("reset", False)
        query_text = prompt_data.get("prompt", "")

        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(SCRIPT_DIR), ALLOWED_MODELS)
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        loaded_models = config.get("models", [])
        if not loaded_models:
            raise ValueError("No models found in allowed_models.json")
        model = loaded_models[model_index]
        model_id = model["id"]

        manager = LLMManager()
        try:
            manager.start_model_container(model_id)
            if reset:
                print("✨ Clearing Database")
                self.clear_database()

            # Create (or update) the data store.
            documents = self.load_documents()
            chunks = self.split_documents(documents)
            db = self.add_to_chroma(chunks)

            # Query using the prompt
            response_text = self.query_rag(query_text, manager, model_id)
            prompt_data["rag_response"] = response_text
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            raise
        finally:
            print("\n🧹 Cleaning up...")
            if db and hasattr(db, "close"):
                db.close()
            if os.path.exists(CHROMA_PATH):
                shutil.rmtree(CHROMA_PATH)
            manager.stop_model_container(model_id)
            print("✅ Cleanup complete")
        return prompt_data

    def load_documents(self):
        # Always re-clone the GitHub repo to ensure it's up to date
        if CLONE_PATH.exists():
            print(f"Removing existing cloned repo at {CLONE_PATH}...")
            shutil.rmtree(CLONE_PATH)
        print(f"Cloning GitHub repo to {CLONE_PATH}...")
        subprocess.run(
            ["git", "clone", GITHUB_REPO_URL, str(CLONE_PATH)],
            check=True,
        )
        # Load from both local and cloned repo
        loaders = [
            DirectoryLoader(
                str(LOCAL_PATH.absolute()),
                glob="**/*",
                loader_cls=TextLoader,
            ),
            DirectoryLoader(
                str(CLONE_PATH.absolute()),
                glob="**/*",
                loader_cls=TextLoader,
            ),
        ]
        documents = []
        for loader in loaders:
            try:
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading documents: {e}")
        return documents

    def split_documents(self, documents: list[Document]):
        # Splits documents into smaller chunks to fit in the context window
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)

    def get_embedding_function(self):
        # Use local embedding model for offline operation
        # Model is stored locally to avoid internet dependency
        local_model_path = os.path.join(
            os.path.dirname(__file__), 
            "include_project", 
            "models--sentence-transformers--all-MiniLM-L6-v2",
            "snapshots",
            "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"
        )
        
        try:
            # Try to use local model first
            if os.path.exists(local_model_path):
                print(f"Using local embedding model from: {local_model_path}")
                return HuggingFaceEmbeddings(
                    model_name=local_model_path,
                    cache_folder=os.path.dirname(local_model_path)
                )
            else:
                # Fallback to downloading if local model doesn't exist
                print("Local model not found, downloading from HuggingFace...")
                return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        except ImportError:
            print(
                "HuggingFaceEmbeddings not found. "
                "Using OllamaEmbeddings as fallback."
            )
            return OllamaEmbeddings(model="llama2")

    def add_to_chroma(self, chunks: list[Document]):
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=self.get_embedding_function(),
        )

        chunks_with_ids = self.calculate_chunk_ids(chunks)

        # Add or update the documents.
        existing_items = db.get(
            include=[]
        )  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = [
            chunk
            for chunk in chunks_with_ids
            if chunk.metadata["id"] not in existing_ids
        ]
        if len(new_chunks):
            print(f"👉 Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
        return db

    def calculate_chunk_ids(self, chunks):

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

    def clear_database(self):
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
        if CLONE_PATH.exists():
            shutil.rmtree(CLONE_PATH)

    # Query the database
    def query_rag(self, query_text: str, manager, model_id):
        # Prepare the DB.
        embedding_function = self.get_embedding_function()
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_function,
        )

        # Search the DB.
        results = db.similarity_search_with_score(query_text, k=5)
        context_text = "\n\n---\n\n".join(
            [doc.page_content for doc, _score in results]
        )
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(
            context=context_text, question=query_text
        )
        # Use LLMManager to send the prompt to the selected model
        response_text, *_ = manager.send_prompt(model_id, prompt)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        print(formatted_response)
        return response_text


# Still open: Add a function to update the chunk when a file is edited
# A section of this code is inspired by https://github.com/pixegami/rag-tutorial-v2
