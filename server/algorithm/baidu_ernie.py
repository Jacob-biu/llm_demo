import paddle
from paddlenlp.transformers import ErnieTokenizer, ErnieModel
import paddle.nn.functional as F

# 加载Ernie模型和分词器
tokenizer = ErnieTokenizer.from_pretrained('ernie-1.0')
model = ErnieModel.from_pretrained('ernie-1.0')

# 编码输入问题和参考文本
def encode_text(text):
    inputs = tokenizer(text, return_tensors='pd', max_length=128, padding=True, truncation=True)
    with paddle.no_grad():
        outputs = model(**inputs)
        # outputs[0] 是 sequence_output, outputs[1] 是 pooled_output
        # 如果没有 pooled_output，则使用 sequence_output 的均值
        if isinstance(outputs, tuple) and len(outputs) > 1:
            pooled_output = outputs[1]  # 使用 pooled_output
        else:
            pooled_output = paddle.mean(outputs[0], axis=1)  # 使用序列输出的均值
    return pooled_output

# 计算余弦相似度
def cosine_similarity_score(embedding1, embedding2):
    return F.cosine_similarity(embedding1, embedding2).numpy()[0]

# 问题和参考文本
question = "简单介绍一下长征"
reference_text = "长征是中国工农红军在 1934-1936 年进行的战略转移"

# 获取编码后的向量
question_embedding = encode_text(question)
reference_embedding = encode_text(reference_text)

# 计算余弦相似度
similarity = cosine_similarity_score(question_embedding, reference_embedding)

# 输出相似度
print(f"余弦相似度: {similarity}")

# 判断是否相关
if similarity > 0.7:
    print("相关")
else:
    print("不相关")
