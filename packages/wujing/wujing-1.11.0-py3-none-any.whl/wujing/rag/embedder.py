import numpy as np
from sentence_transformers import SentenceTransformer, SimilarityFunction
from typing import List, Dict
import warnings


class Embedder:
    def __init__(self, model_path: str = "BAAI/bge-m3"):
        """
        初始化句子嵌入模型

        Args:
            model_path: 预训练模型路径或HuggingFace模型ID
        """
        try:
            self.model = SentenceTransformer(model_path, similarity_fn_name=SimilarityFunction.COSINE)
            # Test the model with a simple sentence
            test_embedding = self.model.encode(["test sentence"])
            if not isinstance(test_embedding, np.ndarray):
                warnings.warn(f"Model output format unexpected: {type(test_embedding)}")
        except Exception as e:
            raise ValueError(f"Failed to load model from {model_path}: {str(e)}")

    def encode(self, sentences: List[str], normalize_embeddings: bool = True) -> np.ndarray:
        """
        将输入句子编码为嵌入向量

        Args:
            sentences: 要编码的句子列表
            normalize_embeddings: 是否将嵌入向量归一化为单位长度

        Returns:
            形状为 (num_sentences, embedding_dim) 的numpy数组
        """
        if not sentences:
            return np.array([])

        try:
            embeddings = self.model.encode(sentences, normalize_embeddings=normalize_embeddings, convert_to_numpy=True)
        except Exception as e:
            raise RuntimeError(f"Encoding failed: {str(e)}")

        return embeddings

    def get_top_similar(self, query: str, corpus: List[str], top_k: int = 3) -> List[Dict]:
        """
        获取查询文本在文本集合中最相似的top_k个候选

        Args:
            query: 查询文本
            corpus: 候选文本集合
            top_k: 返回最相似的前k个结果

        Returns:
            包含相似度、文本和排名的字典列表，按相似度降序排列
        """
        if not corpus:
            return []

        # Encode all sentences
        query_embedding = self.encode([query])
        corpus_embeddings = self.encode(corpus)

        # Compute cosine similarity (embeddings are already normalized)
        similarities = np.dot(corpus_embeddings, query_embedding.T).flatten()

        # Get top k results
        top_k = min(top_k, len(corpus))
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = [{"text": corpus[idx], "score": float(similarities[idx]), "rank": rank + 1} for rank, idx in enumerate(top_indices)]

        return results


if __name__ == "__main__":
    embedder = Embedder("./../../../models/BAAI/bge-m3")
    query = "你今天好漂亮."
    corpus = [
        "A man is eating food.",
        "A man is eating a piece of bread.",
        "The girl is carrying a baby.",
        "A man is riding a horse.",
        "A woman is playing violin.",
        "Two men pushed carts through the woods.",
        "A man is riding a white horse on an enclosed ground.",
        "A monkey is playing drums.",
        "A cheetah is running behind its prey.",
        "The spaghetti's been eaten.",
        "A man is eating spaghetti.",
        "A man is drink water.",
        "You look so beautiful today",
        "You look a bit beautiful today",
        "تبدين جميلة اليوم",
        "أنت جميلة جدا اليوم",
    ]

    print(f"Query: {query}")
    top_results = embedder.get_top_similar(query, corpus, top_k=3)

    # Print results
    print("\nTop results:")
    for result in top_results:
        print(f"Rank {result['rank']}:")
        print(f"  Text: {result['text']}")
        print(f"  Score: {result['score']:.4f}")
        print("-" * 60)
