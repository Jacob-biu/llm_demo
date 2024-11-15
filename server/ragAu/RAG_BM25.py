from flask import Flask, request, jsonify
import pandas as pd
import logging
import os
import re
from rank_bm25 import BM25Okapi
import thulac  # 仅用于中文处理

# 设置日志，输出到文件
current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)
log_file_path = os.path.join(current_folder_path, "RAGassessment_bm25.log")
logging.basicConfig(
    filename=log_file_path,
    filemode='a',  # 追加模式
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
app = Flask(__name__)

class PDFTokenizer:
    def __init__(self, language='en'):
        self.language = language
        if language == 'zh':
            self.thu = thulac.thulac()

    def tokenize(self, text):
        if self.language == 'zh':
            result = self.thu.cut(text, text=False)
            words = [word[0] for word in result]
        else:
            words = text.split()  # 对英文文本直接用空格进行分词
        return words

    def truncate_text(self, text, max_length=25):
        if len(text) > max_length:
            return text[:max_length] + '...'
        return text

    def calculate_user_system_bm25_similarities(self, user_question_raw, system_answers_raw):
        user_question_tokens = self.tokenize(user_question_raw)
        system_answers_tokens = [self.tokenize(system_answers_raw)]
        logging.info(f"system_answers_tokens: {system_answers_tokens}\n")
        if not any(system_answers_tokens):  # 检查所有系统回答的分词结果
            raise ValueError("所有系统回答的分词结果为空，请检查输入。")

        logging.info("1\n")

        # 创建 BM25 模型
        bm25 = BM25Okapi(system_answers_tokens)  # 将系统回答作为文档集合
        similarity_user_system = bm25.get_scores(user_question_tokens)
        logging.info(f"用户问题分词: {user_question_tokens}, 系统回答分词: {system_answers_tokens}")
        logging.info(f"BM25计算出的相似度: {similarity_user_system[0]:.6f}")

        if not similarity_user_system[0]:
            raise ValueError("没有计算出相似度，请检查输入的文档和查询。")

        # 过滤掉相似度为0的回答
        return similarity_user_system[0]

    def calculate_user_reference_bm25_similarities(self, user_question_raw, reference_sentences):
        user_question_tokens = self.tokenize(user_question_raw)
        results = []
        # 使用 BM25 计算用户问题与参考句子之间的相似度
        bm25 = BM25Okapi(reference_sentences)  # 参考句子作为文档集合
        scores = bm25.get_scores(user_question_tokens)
        for reference, score in zip(reference_sentences, scores):
            if score > 0:  # 仅记录相似度大于0的结果
                reference_text = ' '.join(reference)
                results.append({
                    "user_question": self.truncate_text(user_question_raw),
                    "reference_text": self.truncate_text(reference_text),
                    "similarity_user_reference": score
                })
        return pd.DataFrame(results)

def detect_language(text):
    if re.search(r'[\u4e00-\u9fff]', text):
        return 'zh'
    else:
        return 'en'

@app.route('/calculate_user_system_similarity', methods=['POST'])
def calculate_user_system_similarity():
    data = request.json
    user_question_raw = data.get('user_question')
    system_answers_raw = data.get('system_answer')
    if not user_question_raw or not system_answers_raw:
        logging.error("缺少必要的参数")
        return jsonify({"error": "缺少必要的参数"}), 400

    logging.info(f"用户问题: {user_question_raw}, 系统回答: {system_answers_raw}")
    language = detect_language(user_question_raw)
    tokenizer = PDFTokenizer(language=language)
    try:
        similarity = tokenizer.calculate_user_system_bm25_similarities(user_question_raw, system_answers_raw)
        logging.info(f"相似度计算结果: {similarity}, 类型: {type(similarity)}")
        return jsonify({"similarity_user_system": float(similarity)})
    except ValueError as e:
        logging.error(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}")
        return jsonify({"error": f"发生了错误: {str(e)}"}), 500



@app.route('/calculate_user_reference_similarity', methods=['POST'])
def calculate_user_reference_similarity():
    data = request.json
    user_question_raw = data.get('user_question')
    reference_texts = data.get('reference_texts', [])
    if not user_question_raw or not reference_texts:
        return jsonify({"error": "缺少必要的参数"}), 400

    language = detect_language(user_question_raw)
    tokenizer = PDFTokenizer(language=language)
    reference_sentences = [tokenizer.tokenize(ref) for ref in reference_texts]
    # 确保参考句子不为空
    if not reference_sentences:
        return jsonify({"error": "参考句子列表为空，请提供有效的参考文本。"}), 400

    results_df = tokenizer.calculate_user_reference_bm25_similarities(user_question_raw, reference_sentences)
    response_data = results_df.to_dict(orient='records')
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
