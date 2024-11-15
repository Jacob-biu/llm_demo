from flask import Flask, request, jsonify
import json
import paddle
from paddlenlp.transformers import ErnieTokenizer, ErnieModel
import re
import thulac
import pandas as pd  # 确保导入 pandas
from tabulate import tabulate
import paddle.nn.functional as F
import logging
import os

# 设置日志，输出到文件
current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)
log_file_path = os.path.join(current_folder_path, "RAGassessment_ernie.log")
logging.basicConfig(
    filename=log_file_path,
    filemode='a',  # 追加模式
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)

class PDFTokenizer:
    def __init__(self):
        self.thu = thulac.thulac()
        self.tokenizer = ErnieTokenizer.from_pretrained('ernie-1.0')
        self.model = ErnieModel.from_pretrained('ernie-1.0')

    def tokenize(self, text):
        result = self.thu.cut(text, text=False)
        words = [word[0] for word in result]
        return words

    def encode_text(self, text):
        inputs = self.tokenizer(text, return_tensors='pd', max_length=128, padding=True, truncation=True)
        with paddle.no_grad():
            outputs = self.model(**inputs)
            return outputs[1]  # 使用 pooled_output

    def cosine_similarity_score(self, embedding1, embedding2):
        return F.cosine_similarity(embedding1, embedding2).numpy()[0]

    def truncate_text(self, text, max_length=25):
        """将文本截断到最大长度，并在末尾加省略号"""
        if len(text) > max_length:
            return text[:max_length] + '...'
        return text

    def calculate_similarities(self, user_question_raw, system_answer_raw, reference_sentences):
        # 获取用户问题的向量
        user_question_embedding = self.encode_text(user_question_raw)

        # 获取系统回答的向量
        system_answer_embedding = self.encode_text(system_answer_raw)

        # 计算用户问题与系统回答之间的余弦相似度
        similarity_user_system = self.cosine_similarity_score(user_question_embedding, system_answer_embedding)

        # 初始化比较结果
        results = []

        # 计算参考文本与用户问题/系统回答的相似度并收集结果
        for reference in reference_sentences:
            reference_text = ' '.join(reference)
            reference_embedding = self.encode_text(reference_text)

            # 计算用户问题与参考文本的相似度
            similarity_user_reference = self.cosine_similarity_score(user_question_embedding, reference_embedding)

            # 计算系统回答与参考文本的相似度
            similarity_system_reference = self.cosine_similarity_score(system_answer_embedding, reference_embedding)

            results.append({
                "用户问题": self.truncate_text(user_question_raw),  # 限制长度
                "参考句子": self.truncate_text(reference_text),     # 限制长度
                "系统回答": self.truncate_text(system_answer_raw),  # 限制长度
                "用户问题与参考文字相似度": similarity_user_reference,
                "系统回答与参考文字相似度": similarity_system_reference
            })

        # 添加用户问题与系统回答的相似度
        results.append({
            "用户问题": self.truncate_text(user_question_raw),  # 限制长度
            "系统回答": self.truncate_text(system_answer_raw),  # 限制长度
            "用户问题与系统回答相似度": similarity_user_system
        })

        # 返回结果作为 DataFrame
        return pd.DataFrame(results)

@app.route('/calculate_similarity', methods=['POST'])
def calculate_similarity():
    # 获取请求数据
    data = request.json
    user_question_raw = data.get('user_question')
    system_answer_raw = data.get('system_answer')
    reference_texts = data.get('reference_texts', [])

    if not user_question_raw or not system_answer_raw or not reference_texts:
        return jsonify({"error": "缺少必要的参数"}), 400

    # 实例化 PDFTokenizer
    tokenizer = PDFTokenizer()

    # 分词处理参考文本
    reference_sentences = [tokenizer.tokenize(ref) for ref in reference_texts]
    
    # 计算相似度
    results_df = tokenizer.calculate_similarities(user_question_raw, system_answer_raw, reference_sentences)

    # 将结果限制为字符串形式并创建表格
    table = tabulate(results_df, headers='keys', tablefmt='grid')

    print(table)

    # 输出到日志，说明来源
    logging.info(f"来自 ernie_server 的计算结果:\n{table}\n")

    # 返回结果，确保为 UTF-8 编码
    response_data = results_df.to_dict(orient='records')
    response = json.dumps(response_data, ensure_ascii=False)  # 设置 ensure_ascii=False
    return app.response_class(response, content_type='application/json; charset=utf-8')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # 在 5000 端口运行 Flask 服务器









# import paddle
# from paddlenlp.transformers import ErnieTokenizer, ErnieModel
# import pdfplumber
# import thulac
# import os
# import logging
# import re
# import pandas as pd  # 确保导入 pandas
# from tabulate import tabulate
# import paddle.nn.functional as F

# # 设置日志，输出到文件
# current_file_path = os.path.abspath(__file__)
# current_folder_path = os.path.dirname(current_file_path)
# log_file_path = os.path.join(current_folder_path, "RAGassessment_ernie.log")
# logging.basicConfig(
#     filename=log_file_path,
#     filemode='a',  # 追加模式
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# class PDFTokenizer:
#     def __init__(self, path):
#         self.path = path
#         self.thu = thulac.thulac()
#         self.tokenizer = ErnieTokenizer.from_pretrained('ernie-1.0')
#         self.model = ErnieModel.from_pretrained('ernie-1.0')

#     def read_pdf(self, pdf_path):
#         text = ""
#         try:
#             with pdfplumber.open(pdf_path) as pdf:
#                 for page in pdf.pages:
#                     page_text = page.extract_text()
#                     if page_text:
#                         text += page_text
#         except Exception as e:
#             logging.error(f"读取 PDF 文件 {pdf_path} 时出错: {e}")
#             raise
#         return text

#     def read_text_file(self, text_file):
#         try:
#             with open(text_file, "r", encoding="utf-8") as f:
#                 return f.read()
#         except Exception as e:
#             logging.error(f"读取文本文件 {text_file} 时出错: {e}")
#             raise

#     def tokenize(self, text):
#         result = self.thu.cut(text, text=False)
#         words = [word[0] for word in result]
#         return words

#     def process_files(self):
#         words = {}
#         for filename in os.listdir(self.path):
#             file_path = os.path.join(self.path, filename)
#             if filename.endswith('.pdf'):
#                 text = self.read_pdf(file_path)
#             elif filename.endswith('.txt'):
#                 text = self.read_text_file(file_path)
#             else:
#                 continue
            
#             # 按句子分割
#             sentences = re.split(r'(?<=[。！？])', text)
#             words[filename] = [self.tokenize(sentence) for sentence in sentences if sentence.strip()]
        
#         return words

#     def encode_text(self, text):
#         inputs = self.tokenizer(text, return_tensors='pd', max_seq_len=128, padding=True, truncation=True)
#         with paddle.no_grad():
#             outputs = self.model(**inputs)
#             return outputs[1]  # 使用 pooled_output

#     def cosine_similarity_score(self, embedding1, embedding2):
#         return F.cosine_similarity(embedding1, embedding2).numpy()[0]

#     def calculate_similarities(self):
#         words = self.process_files()
#         print("分词结果:", words)

#         # 从 user_question.txt 文件读取用户问题
#         user_question_file_path = os.path.join(system_user_folder_path, 'user_question.txt')
#         with open(user_question_file_path, "r", encoding="utf-8") as f:
#             user_question_raw = f.read().strip()

#         # 获取用户问题的向量
#         user_question_embedding = self.encode_text(user_question_raw)

#         # 读取系统回答
#         system_answer_file_path = os.path.join(system_user_folder_path, 'system_answer.txt')
#         with open(system_answer_file_path, "r", encoding="utf-8") as f:
#             system_answer_raw = f.read().strip()

#         # 获取系统回答的向量
#         system_answer_embedding = self.encode_text(system_answer_raw)

#         # 计算用户问题与系统回答之间的余弦相似度
#         similarity_user_system = self.cosine_similarity_score(user_question_embedding, system_answer_embedding)

#         # 初始化比较结果
#         results = []

#         # 计算参考文本与用户问题/系统回答的相似度并收集结果
#         for file, sentences in words.items():
#             for reference in sentences:
#                 reference_text = ' '.join(reference)
#                 reference_embedding = self.encode_text(reference_text)

#                 # 计算用户问题与参考文本的相似度
#                 similarity_user_reference = self.cosine_similarity_score(user_question_embedding, reference_embedding)

#                 # 计算系统回答与参考文本的相似度
#                 similarity_system_reference = self.cosine_similarity_score(system_answer_embedding, reference_embedding)

#                 results.append({
#                     "用户问题": user_question_raw,
#                     "参考句子": reference_text,
#                     "系统回答": system_answer_raw,
#                     "用户问题与参考文字相似度": similarity_user_reference,
#                     "系统回答与参考文字相似度": similarity_system_reference
#                 })

#         # 添加用户问题与系统回答的相似度
#         results.append({
#             "用户问题": user_question_raw,
#             "系统回答": system_answer_raw,
#             "用户问题与系统回答相似度": similarity_user_system
#         })

#         # 创建 DataFrame 并打印结果表格
#         results_df = pd.DataFrame(results)

#         # 限制表格内容长度
#         def truncate_text(text, max_length=20):
#             return text if len(text) <= max_length else text[:max_length] + '...'
        
#         df = results_df.applymap(lambda x: truncate_text(str(x)))

#         # 使用 tabulate 创建带边框线条的表格
#         table = tabulate(df, headers='keys', tablefmt='grid')

#         logger = logging.getLogger()

#         # 输出表格到日志
#         logger.info("\n" + table + "\n")

#         print(table)

# # 使用示例
# if __name__ == "__main__":
#     # 设定文件夹路径
#     file_folder_path = os.path.join(current_folder_path, 'file')
#     system_user_folder_path = os.path.join(current_folder_path, 'system_user')

#     # 实例化 PDFTokenizer 并计算相似度
#     tokenizer = PDFTokenizer(path=file_folder_path)
    
#     try:
#         tokenizer.calculate_similarities()
#     except Exception as e:
#         print(f"发生错误: {e}")
