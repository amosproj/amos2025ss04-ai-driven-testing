from modules.base import ModuleBase
import os
import shutil
import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader, PythonLoader
from langchain.prompts import ChatPromptTemplate
from llm_manager import LLMManager

CHROMA_PATH = "chroma"
ALLOWED_MODELS = "allowed_models.json"
PROMPT_TEMPLATE = """
Answer the query based only on the following context:
{context}
---
Answer the query based on the above context: {question}
"""

class IncludeProjectModule(ModuleBase):
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
            if db and hasattr(db, 'close'):
                db.close()
            if os.path.exists(CHROMA_PATH):
                shutil.rmtree(CHROMA_PATH)
            manager.stop_model_container(model_id)
            print("✅ Cleanup complete")
        return prompt_data

    def load_documents(self):
        # Opens the Python files in the directory
        abs_path = Path(__file__).parent.parent / "../python-test-cases"
        document_loader = DirectoryLoader(
            str(abs_path.absolute()),
            glob="**/*.py",
            loader_cls=PythonLoader
        )
        return document_loader.load()

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
        # Other open-source embeddings can be used to enhance performance, if necessary
        # https://python.langchain.com/docs/integrations/text_embedding/
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        return embeddings

    def add_to_chroma(self, chunks: list[Document]):
        db = Chroma(
            persist_directory=CHROMA_PATH, embedding_function=self.get_embedding_function()
        )

        chunks_with_ids = self.calculate_chunk_ids(chunks)

        # Add or update the documents.
        existing_items = db.get(include=[]) # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]
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

    
    # Query the database
    def query_rag(self, query_text: str, manager, model_id):
        # Prepare the DB.
        embedding_function = self.get_embedding_function()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
        # Search the DB.
        results = db.similarity_search_with_score(query_text, k=5)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        # Use LLMManager to send the prompt to the selected model
        response_text, *_ = manager.send_prompt(model_id, prompt)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        print(formatted_response)
        return response_text


# Still open: Add a function to update the chunk when a file is edited
# A section of this code is inspired by https://github.com/pixegami/rag-tutorial-v2
