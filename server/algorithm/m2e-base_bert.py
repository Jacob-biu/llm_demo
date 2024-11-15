import logging
import os
import numpy as np
from paddlenlp.transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import torch

# 获取当前文件的目录
current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)
log_file_path = os.path.join(current_folder_path, "app.log")

# 配置日志记录
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# 捕获所有未处理的异常，并记录到日志文件中
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

import sys
sys.excepthook = handle_exception

# 加载本地 GloVe 模型
def load_glove_model(file_path):
    model = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            split_line = line.split()
            word = split_line[0]
            embedding = np.array([float(val) for val in split_line[1:]])
            model[word] = embedding
    return model

glove_model = load_glove_model('path_to_glove_file/glove.6B.300d.txt')

# 加载 m2e-bert 模型和分词器
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
bert_model = BertModel.from_pretrained('bert-base-chinese')

# 定义文本向量化函数
def text_to_vector(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    last_hidden_state = outputs[0]
    vector = last_hidden_state.mean(dim=1)
    return vector.numpy()

# GloVe 嵌入向量化函数
def get_glove_vector(text, model):
    tokens = text.split()
    vectors = [model[token] for token in tokens if token in model]
    return np.mean(vectors, axis=0)

# 输入问题和参考文本
question = "这是你的问题"
reference_texts = [
    "这是第一个参考文本。",
    "这是第二个参考文本。",
    "这是一个不同的参考文本。"
]

# GloVe 文本向量化
glove_vectors = [get_glove_vector(text, glove_model) for text in reference_texts]
glove_question_vector = get_glove_vector(question, glove_model)

# m2e-bert 文本向量化
m2e_bert_question_vector = text_to_vector(question, bert_model, bert_tokenizer)
m2e_bert_reference_vectors = np.array([text_to_vector(text, bert_model, bert_tokenizer) for text in reference_texts]).squeeze()

# 计算余弦相似度
glove_cos_sim = cosine_similarity([glove_question_vector], glove_vectors)
m2e_bert_cos_sim = cosine_similarity(m2e_bert_question_vector, m2e_bert_reference_vectors)

# 使用 BM25 计算相似度
bm25 = BM25Okapi([text.split() for text in reference_texts])
bm25_scores = bm25.get_scores(question.split())

# 输出相似度比较结果
logger.info(f"GloVe 余弦相似度: {glove_cos_sim}")
logger.info(f"m2e-bert 余弦相似度: {m2e_bert_cos_sim}")
logger.info(f"BM25 相似度: {bm25_scores}")

print("GloVe 余弦相似度:", glove_cos_sim)
print("m2e-bert 余弦相似度:", m2e_bert_cos_sim)
print("BM25 相似度:", bm25_scores)
