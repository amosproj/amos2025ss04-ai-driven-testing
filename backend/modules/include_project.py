from modules.base import ModuleBase
import os
import shutil
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.prompts import ChatPromptTemplate
from schemas import PromptData, ResponseData

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

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        query_text = prompt_data.input.user_message
        reset = getattr(prompt_data, "reset", False)

        if reset:
            print("✨ Clearing database")
            self.clear_database()

        documents = self.load_documents()
        chunks = self.split_documents(documents)
        self.add_to_chroma(chunks)

        # Get enhanced prompt from Chroma
        rag_prompt, sources = self.query_rag(query_text)

        # Save into schema fields
        prompt_data.rag_prompt = rag_prompt
        prompt_data.rag_sources = sources

        # Optionally override the user message to use the RAG prompt directly
        prompt_data.input.user_message = rag_prompt

        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        print("\n🧹 Cleaning up...")
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
        if CLONE_PATH.exists():
            shutil.rmtree(CLONE_PATH)
        # If you need to stop the model container, you may need to pass manager/model_id here
        print("✅ Cleanup complete")
        return response_data

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

    def get_embedding_function(self, model_index=0):
        # Always use nomic-embed-text for embeddings
        embedding_model = "nomic-embed-text"
        print(
            f"Using OllamaEmbeddings for embeddings with model: {embedding_model}"
        )
        return OllamaEmbeddings(model=embedding_model)

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
    def query_rag(self, query_text: str):
        # Prepare the DB.
        embedding_function = self.get_embedding_function()
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_function,
        )

        # Search the DB.
        results = db.similarity_search_with_score(query_text, k=10)
        context_text = "\n\n---\n\n".join(
            [doc.page_content for doc, _score in results]
        )
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(
            context=context_text, question=query_text
        )

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        # Return the prompt and sources, do NOT call the LLM here
        return prompt, sources


# Still open: Add a function to update the chunk when a file is edited
# A section of this code is inspired by https://github.com/pixegami/rag-tutorial-v2
