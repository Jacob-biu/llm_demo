import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import pdfplumber
import thulac
import os
import logging
import re
import pandas as pd  # 确保导入 pandas
from tabulate import tabulate

# 计算 BLEU 分数
smoothing_function = SmoothingFunction()

# 设置日志，输出到文件
current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)
log_file_path = os.path.join(current_folder_path, "RAGassessment_bleu.log")
logging.basicConfig(
    filename=log_file_path,
    filemode='a',  # 追加模式
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class PDFTokenizer:
    def __init__(self, path):
        self.path = path
        self.thu = thulac.thulac()

    def read_pdf(self, pdf_path):
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
        except Exception as e:
            logging.error(f"读取 PDF 文件 {pdf_path} 时出错: {e}")
            raise
        return text

    def read_text_file(self, text_file):
        try:
            with open(text_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logging.error(f"读取文本文件 {text_file} 时出错: {e}")
            raise

    def tokenize(self, text):
        result = self.thu.cut(text, text=False)
        words = [word[0] for word in result]
        return words

    def process_files(self):
        words = {}
        for filename in os.listdir(self.path):
            file_path = os.path.join(self.path, filename)
            if filename.endswith('.pdf'):
                text = self.read_pdf(file_path)
            elif filename.endswith('.txt'):
                text = self.read_text_file(file_path)
            else:
                continue
            
            # 按句子分割
            sentences = re.split(r'(?<=[。！？])', text)
            words[filename] = [self.tokenize(sentence) for sentence in sentences if sentence.strip()]
        
        return words

# 使用示例
file_folder_path = os.path.join(current_folder_path, 'file')
system_user_folder_path = os.path.join(current_folder_path, 'system_user')
tokenizer = PDFTokenizer(path=file_folder_path)

try:
    words = tokenizer.process_files()
    print("分词结果:", words)
    
    # 从 user_question.txt 文件读取用户问题
    user_question_file_path = os.path.join(system_user_folder_path, 'user_question.txt')
    with open(user_question_file_path, "r", encoding="utf-8") as f:
        user_question_raw = f.read().strip()

    # 处理用户问题
    user_question = " ".join([word[0] for word in tokenizer.thu.cut(user_question_raw, text=False)])

    # 读取系统回答
    system_answer_file_path = os.path.join(system_user_folder_path
    , 'system_answer.txt')
    with open(system_answer_file_path, "r", encoding="utf-8") as f:
        system_answer_raw = f.read().strip()

    # 处理系统回答
    system_answer = " ".join([word[0] for word in tokenizer.thu.cut(system_answer_raw, text=False)])

    # 计算用户问题与系统回答之间的 BLEU 分数
    user_candidate = user_question.split()
    system_candidate = system_answer.split()
    bleu_score_user_system = sentence_bleu([system_candidate], user_candidate, smoothing_function=smoothing_function.method1)

    # 初始化比较结果
    results = []

    # 计算 BLEU 分数并收集结果
    for file, sentences in words.items():
        for reference in sentences:
            candidate = user_question.split()
            bleu_score_user = sentence_bleu([reference], candidate, smoothing_function=smoothing_function.method1)

            bleu_score_system = sentence_bleu([reference], system_candidate, smoothing_function=smoothing_function.method1)

            results.append({
                "用户问题": user_question,
                "参考句子": ' '.join(reference),
                "系统回答": system_answer,
                "用户问题与参考文字 BLEU 分数": bleu_score_user,
                "系统回答与参考文字 BLEU 分数": bleu_score_system
            })

    # 添加用户问题与系统回答的 BLEU 分数
    results.append({
        "用户问题": user_question,
        "系统回答": system_answer,
        "用户问题与系统回答 BLEU 分数": bleu_score_user_system
    })

    # 创建 DataFrame 并打印结果表格
    results_df = pd.DataFrame(results)

    # 限制表格内容长度
    def truncate_text(text, max_length=20):
        return text if len(text) <= max_length else text[:max_length] + '...'
    
    df = results_df.applymap(lambda x: truncate_text(str(x)))

    # 使用 tabulate 创建带边框线条的表格
    table = tabulate(df, headers='keys', tablefmt='grid')

    logger = logging.getLogger()

    # 输出表格到日志
    logger.info("\n" + table + "\n")

    print(table)

    # 可选：将结果保存为 CSV 文件
    # df.to_csv("bleu_scores_comparison.csv", index=False)

except Exception as e:
    print(f"发生错误: {e}")