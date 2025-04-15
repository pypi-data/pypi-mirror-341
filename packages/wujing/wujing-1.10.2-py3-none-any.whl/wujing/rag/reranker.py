import numpy as np
from sentence_transformers.cross_encoder import CrossEncoder
from typing import List, Dict
import warnings


class CrossEncoderReranker:
    def __init__(self, model_path: str = "BAAI/bge-reranker-v2-m3", top_k: int = 3):
        """
        初始化交叉编码器重排序器

        Args:
            model_path: 预训练模型路径或HuggingFace模型ID
            top_k: 返回最相似的前k个结果
        """
        try:
            self.model = CrossEncoder(model_path, trust_remote_code=True)
            test_scores = self.model.predict([["test", "test"]])
            if not isinstance(test_scores, np.ndarray):
                warnings.warn(f"Model output format unexpected: {type(test_scores)}")
        except Exception as e:
            raise ValueError(f"Failed to load model from {model_path}: {str(e)}")

        self.top_k = min(top_k, 10)

    def get_top_similar(self, query: str, corpus: List[str]) -> List[Dict]:
        """
        获取查询文本在文本集合中最相似的top_k个候选

        Args:
            query: 查询文本
            corpus: 候选文本集合

        Returns:
            包含相似度和文本的字典列表，按相似度降序排列
        """
        if not corpus:
            return []

        sentence_pairs = [[query, sentence] for sentence in corpus]

        try:
            scores = self.model.predict(sentence_pairs)
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}")

        if np.all(scores == scores[0]):
            warnings.warn("All scores are identical, model may not be working properly")

        top_indices = np.argsort(scores)[-self.top_k :][::-1]

        results = [{"text": corpus[idx], "score": float(scores[idx]), "rank": rank + 1} for rank, idx in enumerate(top_indices)]

        return results


if __name__ == "__main__":
    reranker = CrossEncoderReranker("./../../../models/BAAI/bge-reranker-v2-m3", top_k=3)
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
    top_results = reranker.get_top_similar(query, corpus)

    # 打印结果
    print("\nTop results:")
    for result in top_results:
        print(f"Rank {result['rank']}:")
        print(f"  Text: {result['text']}")
        print(f"  Score: {result['score']:.4f}")
        print("-" * 60)
