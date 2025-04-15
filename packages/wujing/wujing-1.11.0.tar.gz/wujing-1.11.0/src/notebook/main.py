import uuid
import chromadb
from chromadb.utils import embedding_functions
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from rich import print as rich_print


class ChromaDBManager:
    def __init__(
        self,
        persist_directory: str = ".diskcache/chroma",
        embedding_model: str = "BAAI/bge-m3",
        device: str = "cuda",
        reset_db: bool = False,
    ):
        self.embedding_model = embedding_model
        self.device = device

        self.db_dir = Path(persist_directory).absolute()
        if reset_db:
            try:
                if self.db_dir.exists():
                    shutil.rmtree(self.db_dir)
            except FileNotFoundError:
                rich_print("[red]Directory not found, skipping removal.[/red]")
            except Exception as e:
                rich_print(f"[red]An error occurred: {e}[/red]")

        # Initialize client and collection
        self.client = chromadb.PersistentClient(path=self.db_dir.as_posix())
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.embedding_model,
            device=self.device,
        )

    def upsert(self, collection_name: str, documents: List[str], metadata: Optional[List[Dict]] = None) -> List[str]:
        collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
        )

        ids = [str(uuid.uuid4()) for _ in documents]

        collection.upsert(
            documents=documents,
            metadatas=metadata,
            ids=ids,
        )
        return ids

    def query(
        self,
        query_texts: List[str],
        n_results: int = 5,
        include: List[str] = ["documents", "metadatas", "distances"],
    ) -> Dict:
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            include=include,
        )

    def reset_collection(self, collection_name: str):
        self.client.delete_collection(name=collection_name)


# Example usage
if __name__ == "__main__":
    # Initialize with default settings
    db_manager = ChromaDBManager(reset_db=True)

    # Add some documents
    documents = ["This is a document about pineapple", "This is a document about oranges"]
    db_manager.add_documents(documents)

    # Query and print results
    db_manager.print_query_results(["oranges"], n_results=1)
