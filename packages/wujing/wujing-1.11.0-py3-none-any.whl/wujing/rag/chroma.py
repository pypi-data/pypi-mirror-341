import rich
import uuid
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from typing import List, Dict, Optional
from chromadb.config import Settings


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

        self.client = chromadb.PersistentClient(
            path=self.db_dir.as_posix(),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            ),
        )

        if reset_db:
            self.client.reset()

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
        collection_name: str,
        query_texts: List[str],
        n_results: int = 5,
        include: List[str] = ["documents", "metadatas", "distances"],
    ) -> Dict:
        collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
        )

        return collection.query(
            query_texts=query_texts,
            n_results=n_results,
            include=include,
        )

    def reset_collection(self, collection_name: str):
        self.client.delete_collection(name=collection_name)


if __name__ == "__main__":
    db_manager = ChromaDBManager(
        embedding_model="./../../../models/BAAI/bge-m3",
        reset_db=True,
        persist_directory=".diskcache/chroma2",
    )
    db_manager.upsert(
        "collection",
        [
            "This is a document about pineapple",
            "This is a document about oranges",
        ],
    )
    rich.print(
        db_manager.query(
            "collection",
            ["oranges", "red"],
            n_results=3,
        )
    )
