import nltk
from nltk.translate.bleu_score import sentence_bleu
import pdfplumber
import thulac
import os
import logging
import re
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# 计算 BLEU 分数
smoothing_function = SmoothingFunction()


# 下载 NLTK 的数据（只需运行一次）
# nltk.download('punkt')

# 设置日志，输出到文件
current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)
log_file_path = os.path.join(current_folder_path, "assessment.log")
logging.basicConfig(
    filename=log_file_path,
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
            logging.error(f"Error reading PDF file {pdf_path}: {e}")
            raise
        return text

    def read_text_file(self, text_file):
        try:
            with open(text_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error reading text file {text_file}: {e}")
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
# folder_path = "./file"  # 指定文件夹路径
file_folder_path = os.path.join(current_folder_path, 'file')
tokenizer = PDFTokenizer(path=file_folder_path)

try:
    words = tokenizer.process_files()
    print("分词结果:", words)
    
    # 示例用户问题候选
    user_questions_raw = [
        "这是用户问题候选一？",
        "这是一个测试文本。",
    ]

    # 对用户问题进行分词
    user_questions = [" ".join([word[0] for word in tokenizer.thu.cut(q, text=False)]) for q in user_questions_raw]

    # 计算 BLEU 分数
    for user_question in user_questions:
        print(f"用户问题候选: {user_question}")
        for file, sentences in words.items():
            for reference in sentences:
                # 将句子分词为单词
                candidate = user_question.split()
                
                # 计算 BLEU 分数
                bleu_score = sentence_bleu([reference], candidate, smoothing_function=smoothing_function.method1)
                print(f"  与参考文件 '{file}' 的句子 '{' '.join(reference)}' 的 BLEU 分数: {bleu_score:.4f}")

except Exception as e:
    print(f"An error occurred: {e}")
