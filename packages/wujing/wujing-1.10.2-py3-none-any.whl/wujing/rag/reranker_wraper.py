# 导入必要的库
import rich  # 用于美化输出
from tqdm import tqdm  # 用于显示进度条
import ray  # 用于并行计算
from wujing.rag.reranker import CrossEncoderReranker
from diskcache import FanoutCache

cache = FanoutCache(directory="./.diskcache/rerank_queries")


@cache.memoize(typed=True)
def rerank_query(querys, corpus, model_path="BAAI/bge-reranker-v2-m3", num_gpus=8, top_k=3, score_threshold=0.95):
    """
    使用Ray和CrossEncoderReranker进行并行查询重排序

    参数:
        querys: 需要重排序的查询字符串列表
        corpus: 要搜索的语料库
        model_path: 重排序模型的路径，默认为"BAAI/bge-reranker-v2-m3"
        num_gpus: 用于并行处理的GPU数量，默认为8
        top_k: 每个查询返回的顶部结果数量，默认为3
        score_threshold: 结果需要满足的最小分数阈值，默认为0.95

    返回:
        包含查询和满足分数阈值的顶部结果的字典列表
    """
    # 初始化Ray，指定使用的GPU数量
    ray.init(num_gpus=num_gpus)

    # 定义一个Ray Actor类，用于在单个GPU上处理查询
    @ray.remote(num_gpus=1)
    class RerankerActor:
        def __init__(self, model_path):
            # 初始化重排序器
            self.reranker = CrossEncoderReranker(model_path, top_k=top_k)

        def process_query(self, query, corpus):
            # 获取查询的顶部结果
            top_results = self.reranker.get_top_similar(query, corpus)
            # 获取当前最高分数，如果没有结果则分数为0
            current_score = top_results[0]["score"] if top_results else 0
            # 如果最高分数大于阈值，则返回结果
            if current_score > score_threshold:
                return {"query": query, "results": top_results}
            return None

    try:
        # 创建指定数量的RerankerActor实例
        actors = [RerankerActor.remote(model_path) for _ in range(num_gpus)]
        # 将语料库放入Ray的对象存储中，避免重复传输
        corpus_ref = ray.put(corpus)
        # 存储任务引用
        task_refs = []

        # 为每个查询分配一个Actor进行处理
        for i, query in enumerate(querys):
            actor = actors[i % num_gpus]  # 轮询分配Actor
            task_refs.append(actor.process_query.remote(query, corpus_ref))

        # 存储最终结果
        results = []
        # 使用进度条显示处理进度
        with tqdm(total=len(querys)) as pbar:
            while task_refs:
                # 等待任务完成，每次最多返回num_gpus个结果
                done_refs, task_refs = ray.wait(task_refs, num_returns=min(num_gpus, len(task_refs)))

                # 处理完成的任务
                for result in ray.get(done_refs):
                    if result is not None:  # 只保留非空结果
                        results.append(result)

                # 更新进度条
                pbar.update(len(done_refs))

        return results

    finally:
        # 无论是否发生异常，都关闭Ray
        ray.shutdown()


def print_results(results):
    """以格式化的方式打印重排序结果"""
    for item in results:
        rich.print(item["query"])  # 打印查询
        rich.print(item["results"])  # 打印结果
        rich.print("------------------------")  # 打印分隔线


if __name__ == "__main__":
    queries = ["你今天好漂亮."]
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
    results = rerank_query(queries, corpus, model_path="./../../../models/BAAI/bge-reranker-v2-m3")
    print_results(results)
