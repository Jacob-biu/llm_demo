import requests
import json

API_KEY = "y8054zgFMFmXeXZgEXjBNzKy"
SECRET_KEY = "Eb6OLpuVHiFj4lDoHJoHXjR3FgtD2ZSb"

def main():
        
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token=" + get_access_token()
    
    payload = json.dumps({
        "temperature": 0.95,
        "top_p": 0.7,
        "penalty_score": 1,
        "messages": [
            {
                "role": "user",
                "content": "你好"
            },
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.text)
    print(response.json().get('result', {}))
    

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
