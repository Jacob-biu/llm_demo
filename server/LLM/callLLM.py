import requests
import json

# API 服务器地址
API_URL = "http://127.0.0.1:8009/v1/chat/completions"

# 对话历史
history = [{"role": "system", "content": "you are a helpful assistant"}]
query = "天空为什么是蓝色的"

# 更新对话历史
history.append({"role": "user", "content": query})

# 构建请求数据
data = {
    "model": "qwen2-7b",
    "messages": history,
    "temperature": 0.8,
    "top_p": 0.95,
    "repetition_penalty": 1.1,
    "stream": True  # 启用流式响应
}

if __name__ == "__main__":
    # 发送请求
    response = requests.post(API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(data))

    # 流式输出的内容
    streamed_content = ""

    # 解析响应
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8').strip()
                if decoded_line.startswith("data: "):
                    data_str = decoded_line[len("data: "):]
                    if data_str != "[DONE]":
                        json_data = json.loads(data_str)
                        if 'choices' in json_data and len(json_data['choices']) > 0:
                            delta = json_data['choices'][0].get('delta', {})
                            content = delta.get('content')
                            if content:
                                streamed_content += content  # 将内容保存到变量中
                                print(content, end='', flush=True)

    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

    # 输出流式响应的完整内容
    print("\n\n完整输出内容：")
    print(streamed_content)
