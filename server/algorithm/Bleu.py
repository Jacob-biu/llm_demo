import os
import logging
from rank_bm25 import BM25Okapi
from paddlenlp.transformers import ErnieTokenizer, ErnieModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import paddle

# 获取当前文件的路径
current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)  # 获取当前文件夹路径

# 设置日志，输出到文件
log_file_path = os.path.join(current_folder_path, "app.log")  # 日志文件的路径
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
)


# 1. 读取指定文件夹下的文档
def load_documents_from_folder(folder_path):
    documents = []
    file_names = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # 尝试用 utf-8 编码读取文件，忽略解码错误
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read().strip()
                documents.append(content)
                file_names.append(file_name)
        except Exception as e:
            logging.error(f"读取文件 {file_name} 时出错: {e}")

    return documents, file_names


# 2. 使用BM25对文档进行初步筛选
def bm25_ranking(documents, query):
    tokenized_docs = [doc.split(" ") for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query = query.split(" ")
    bm25_scores = bm25.get_scores(tokenized_query)
    return bm25_scores


# 3. 使用ERNIE计算文档和问题的语义相似度
def ernie_semantic_similarity(documents, query, tokenizer, model):
    # 编码查询
    query_tokens = tokenizer(query, return_tensors="pd")  # 获取查询的token
    query_embedding = model(**query_tokens)[0][:, 0, :].numpy()  # 获取查询的embedding

    document_embeddings = []
    for doc in documents:
        doc_tokens = tokenizer(doc, return_tensors="pd")  # 获取文档的token
        doc_embedding = model(**doc_tokens)[0][:, 0, :].numpy()  # 获取文档的embedding
        document_embeddings.append(doc_embedding)

    document_embeddings = np.array(document_embeddings).squeeze(1)  # 转换为numpy数组
    cosine_scores = cosine_similarity(query_embedding, document_embeddings)
    return cosine_scores[0]


# 主程序
def main():
    folder_path = "/home/bxliu/miniconda/LLM/llm_demo_0_2_1/llm_demo/server/files/测试"

    # 加载文档
    documents, file_names = load_documents_from_folder(folder_path)
    logging.info("加载的文档: %s", file_names)

    # 定义问题
    query = "The cat is sitting"

    # 加载ERNIE模型和分词器
    try:
        tokenizer = ErnieTokenizer.from_pretrained("ernie-3.0-base-zh")
        model = ErnieModel.from_pretrained("ernie-3.0-base-zh")
    except Exception as e:
        logging.error(f"加载模型时出错: {e}")
        return

    # 计算BM25得分
    bm25_scores = bm25_ranking(documents, query)

    # 计算ERNIE语义相似度得分
    bert_scores = ernie_semantic_similarity(documents, query, tokenizer, model)

    # 综合BM25和ERNIE的得分
    alpha = 0.5  # 可以调整权重
    combined_scores = alpha * bm25_scores + (1 - alpha) * bert_scores

    # 输出结果，按相关性排序
    sorted_indices = np.argsort(combined_scores)[::-1]

    for idx in sorted_indices:
        print(f"文档: {file_names[idx]}, 得分: {combined_scores[idx]}")

    # 记录运行结束，并添加换行
    logging.info("=====================================")


if __name__ == "__main__":
    main()
