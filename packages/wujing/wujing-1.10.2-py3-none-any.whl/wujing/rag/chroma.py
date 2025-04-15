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
        collection_name: str = "collection",
        persist_directory: str = ".diskcache/chroma",
        embedding_model: str = "BAAI/bge-m3",
        device: str = "cuda",
        reset_db: bool = False,
    ):
        """
        Initialize ChromaDB manager.

        Args:
            collection_name: Name of the collection to use/create
            persist_directory: Directory to persist the database
            embedding_model: Path or name of the SentenceTransformer model
            device: Device to use for embedding ('cpu' or 'cuda')
            reset_db: Whether to reset the database if it exists
        """
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.device = device

        # Setup database directory
        self.db_dir = Path(persist_directory).absolute()
        if reset_db and self.db_dir.exists():
            shutil.rmtree(self.db_dir)

        # Initialize client and collection
        self.client = chromadb.PersistentClient(path=self.db_dir.as_posix())
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.embedding_model,
            device=self.device,
        )
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function,
        )

    def add_documents(self, documents: List[str], metadata: Optional[List[Dict]] = None) -> List[str]:
        """
        Add documents to the collection.

        Args:
            documents: List of document texts to add
            metadata: Optional list of metadata dictionaries for each document

        Returns:
            List of generated UUIDs for the added documents
        """
        ids = [str(uuid.uuid4()) for _ in documents]
        self.collection.add(
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
        """
        Query the collection.

        Args:
            query_texts: List of query texts
            n_results: Number of results to return per query
            include: What information to include in results

        Returns:
            Query results dictionary
        """
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            include=include,
        )

    def reset_collection(self):
        """Reset the current collection."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function,
        )

    def print_query_results(self, query_texts: List[str], n_results: int = 5):
        """Print query results in a pretty format using rich."""
        results = self.query(query_texts, n_results)
        rich_print(results)


# Example usage
if __name__ == "__main__":
    # Initialize with default settings
    db_manager = ChromaDBManager(reset_db=True)

    # Add some documents
    documents = ["This is a document about pineapple", "This is a document about oranges"]
    db_manager.add_documents(documents)

    # Query and print results
    db_manager.print_query_results(["oranges"], n_results=1)
