import requests
import json

API_KEY = "y8054zgFMFmXeXZgEXjBNzKy"
SECRET_KEY = "Eb6OLpuVHiFj4lDoHJoHXjR3FgtD2ZSb"

# 存储问答历史记录
qa_history = []

def main():
    while True:
        user_input = input("你想问什么？（输入'退出'结束）: ")
        if user_input.lower() == '退出':
            break

        # 记录用户问题
        qa_history.append({"role": "user", "content": user_input})

        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token=" + get_access_token()
        
        payload = json.dumps({
            "temperature": 0.95,
            "top_p": 0.7,
            "penalty_score": 1,
            "messages": qa_history  # 将问答历史记录发送给模型
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        # 提取模型的回复
        model_response = response.json().get('result', {}).get('content', '')
        print(f"模型回复: {model_response}")

        # 记录模型的回复
        qa_history.append({"role": "assistant", "content": model_response})

        # 调用相似度计算接口
        similarity = calculate_similarity(user_input, model_response)
        print(f"用户问题与系统回答的相似度: {similarity}")

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

def calculate_similarity(user_question, system_answer):
    url = "http://localhost:5000/calculate_user_system_similarity"  # 替换为你的服务器地址
    payload = {
        "user_question": user_question,
        "system_answer": system_answer
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json().get("similarity_user_system")
    else:
        return f"错误: {response.json().get('error')}"

if __name__ == '__main__':
    main()
