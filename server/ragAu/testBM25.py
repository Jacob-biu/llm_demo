from rank_bm25 import BM25Okapi
import thulac  # 仅用于中文处理


class BM25Example:
    def __init__(self, language='zh'):
        self.language = language
        # 这里假设你已经初始化了一个分词工具，例如THULAC
        self.thu = thulac.thulac()  # 初始化THULAC分词工具

    def tokenize(self, text):
        if self.language == 'zh':
            result = self.thu.cut(text, text=False)
            words = [word[0] for word in result]
        else:
            words = text.split()  # 对英文文本直接用空格进行分词
        return words

    def run(self, document, query):
        # 将单个文档放入列表中
        tokenized_documents = [self.tokenize(document)]
        print(tokenized_documents)
        
        # 创建BM25对象
        bm25 = BM25Okapi(tokenized_documents)

        # 使用自定义的查询分词
        user_question_tokens = self.tokenize(query)

        # 计算BM25得分
        scores = bm25.get_scores(user_question_tokens)

        # 输出得分
        print(f"文档的得分: {scores[0]:.6f}")

# 示例使用
document = "你好！有什么需要我帮助的吗？"
print(f"document: {document}\n")
query = "你好"

bm25_example = BM25Example(language='zh')
bm25_example.run(document, query)
