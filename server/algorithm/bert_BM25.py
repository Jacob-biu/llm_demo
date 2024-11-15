import logging
import os
import numpy as np
from rank_bm25 import BM25Okapi
from paddlenlp.transformers import BertTokenizer, BertModel
import re
import sys


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

def split_text_into_sentences(text):
    # 使用正则表达式按句子划分
    sentences = re.split(r'(?<=[。！？])\s*', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

sys.excepthook = handle_exception

# 加载BERT模型和分词器
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
bert_model = BertModel.from_pretrained('bert-base-chinese')

# 从终端获取参考文本
user_input = input("请输入参考文本（多个句子用句号、问号或感叹号分隔）：")
reference_texts = split_text_into_sentences(user_input)

# BM25分词器
def tokenize(text):
    return bert_tokenizer.tokenize(text)

# 对参考文本进行分词
tokenized_reference_texts = [tokenize(text) for text in reference_texts]

# 使用 rank_bm25 构建 BM25 模型
bm25 = BM25Okapi(tokenized_reference_texts)

# 输入问题
question = input("请输入你的问题：")
tokenized_question = tokenize(question)

# 使用BM25计算相关性分数
scores = bm25.get_scores(tokenized_question)

# 找到最相似的参考文本
most_similar_index = np.argmax(scores)
best_reference = reference_texts[most_similar_index]

# 日志记录
logger.info(f"问题: {question}")
logger.info(f"最相似的参考文本: {best_reference}")

print("问题:", question)
print("最相似的参考文本:", best_reference)

logger.info("\n")
