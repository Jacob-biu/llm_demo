from flask import Flask, request, jsonify
import json
import paddle
from paddlenlp.transformers import BertTokenizer, BertModel
import pandas as pd
from tabulate import tabulate
import paddle.nn.functional as F
import logging
import os
import thulac  # 仅用于中文处理
import re

# 设置日志，输出到文件
current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)
log_file_path = os.path.join(current_folder_path, "RAGassessment_bert.log")
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
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
            self.model = BertModel.from_pretrained('bert-base-chinese')
        else:
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.model = BertModel.from_pretrained('bert-base-uncased')

    def tokenize(self, text):
        if self.language == 'zh':
            result = self.thu.cut(text, text=False)
            words = [word[0] for word in result]
        else:
            words = text.split()  # 对英文文本直接用空格进行分词
        return words

    def encode_text(self, text):
        inputs = self.tokenizer(text, return_tensors='pd', max_length=128, padding=True, truncation=True)
        with paddle.no_grad():
            outputs = self.model(**inputs)
            return outputs[1]  # 使用 pooled_output

    def cosine_similarity_score(self, embedding1, embedding2):
        return F.cosine_similarity(embedding1, embedding2).numpy()[0]

    def truncate_text(self, text, max_length=25):
        if len(text) > max_length:
            return text[:max_length] + '...'
        return text

    def calculate_similarities(self, user_question_raw, system_answer_raw):
        user_question_embedding = self.encode_text(user_question_raw)
        system_answer_embedding = self.encode_text(system_answer_raw)

        similarity_user_system = self.cosine_similarity_score(user_question_embedding, system_answer_embedding)

        return float(similarity_user_system)

    def calculate_user_reference_similarities(self, user_question_raw, reference_sentences):
        user_question_embedding = self.encode_text(user_question_raw)

        results = []
        for reference in reference_sentences:
            reference_text = ' '.join(reference)
            reference_embedding = self.encode_text(reference_text)

            similarity_user_reference = self.cosine_similarity_score(user_question_embedding, reference_embedding)

            results.append({
                "user_question": self.truncate_text(user_question_raw),
                "reference_text": self.truncate_text(reference_text),
                "similarity_user_reference": similarity_user_reference
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
    system_answer_raw = data.get('system_answer')

    if not user_question_raw or not system_answer_raw:
        return jsonify({"error": "缺少必要的参数"}), 400

    language = detect_language(user_question_raw)
    tokenizer = PDFTokenizer(language=language)

    similarity = tokenizer.calculate_similarities(user_question_raw, system_answer_raw)

    return jsonify({"similarity_user_system": similarity})

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
    results_df = tokenizer.calculate_user_reference_similarities(user_question_raw, reference_sentences)

    response_data = results_df.to_dict(orient='records')
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
