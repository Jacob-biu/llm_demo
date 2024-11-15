import requests
import json
import os
import logging
from bs4 import BeautifulSoup
import paddle
from paddlenlp.transformers import BertTokenizer, BertModel
import numpy as np
import time

class WebSearch:
    def __init__(self):
        # 配置日志记录
        log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.log")
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

        self.API_KEY = "y8054zgFMFmXeXZgEXjBNzKy"
        self.SECRET_KEY = "Eb6OLpuVHiFj4lDoHJoHXjR3FgtD2ZSb"

        # 加载 BERT 模型和分词器
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        self.model = BertModel.from_pretrained('bert-base-chinese')

    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.API_KEY, "client_secret": self.SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    def filter_content_with_ernie(self, content):
        access_token = self.get_access_token()
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token=" + access_token

        payload = json.dumps({
            "temperature": 0.95,
            "top_p": 0.7,
            "penalty_score": 1,
            "messages": [
                {
                    "role": "user",
                    "content": f"请剔除以下内容中不符合文章大意的部分：{content}"
                },
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)
        self.logger.info(f"API 响应: {response.json()}")

        if response.status_code == 200:
            result = response.json().get('result', {})
            return result if result else '无过滤内容'
        else:
            self.logger.error(f"调用 ERNIE 失败: {response.text}")
            return "无过滤内容"

    def search_baidu(self, query, retries=3, delay=5):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/53.6"
        }
        search_results = []

        for attempt in range(retries):
            try:
                full_url = f"https://www.baidu.com/s?wd={query}"
                response = requests.get(full_url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                results = soup.find_all("h3", class_="t")
                for result in results:
                    title = result.get_text()
                    link_tag = result.find("a")
                    if link_tag is not None:
                        link = link_tag["href"]
                        page_response = requests.get(link, headers=headers)
                        page_soup = BeautifulSoup(page_response.text, "html.parser")
                        content = page_soup.get_text()
                        content = content.replace("\n", " ").replace("\r", " ").strip()
                        search_results.append((title, content))
                    else:
                        self.logger.warning(f"未找到链接，标题: {title}")

                # 记录搜索结果到日志
                self.logger.info(f"找到的搜索结果: {search_results}")
                break
            except (requests.RequestException, requests.ConnectionError) as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(delay)

        if not search_results:
            self.logger.error("Failed to retrieve search results after retries.")
        
        print(f"\n搜索结果数量: {len(search_results)}\n")
        return search_results

    def calculate_relevance(self, query, content_list):
        query_inputs = self.tokenizer([query], return_tensors='pd', max_length=512, truncation=True, padding=True)
        query_outputs = self.model(**query_inputs)
        query_vector = paddle.mean(query_outputs[0], axis=1).numpy()
        
        results = []
        for title, content in content_list:
            content_inputs = self.tokenizer([content], return_tensors='pd', max_length=512, truncation=True, padding=True)
            content_outputs = self.model(**content_inputs)
            content_vector = paddle.mean(content_outputs[0], axis=1).numpy()
            cosine_sim = np.dot(query_vector, content_vector.T) / (np.linalg.norm(query_vector) * np.linalg.norm(content_vector))
            results.append((title, content, float(cosine_sim)))
        
        results.sort(key=lambda x: x[2], reverse=True)
        return results

    def search_and_filter(self, query):
        content_list = self.search_baidu(query)
        if not content_list:
            print("No results found or unable to connect to Baidu.")
            self.logger.error("No results found or unable to connect to Baidu.")
            return []
        
        scored_results = self.calculate_relevance(query, content_list)
        filtered_results = []

        for title, content, score in scored_results[:5]:
            filtered_content = self.filter_content_with_ernie(content)
            filtered_results.append({
                "title": title,
                "score": f"{score:.4f}",
                "filtered_content": filtered_content if filtered_content else "无过滤内容"
            })

        return filtered_results

if __name__ == "__main__":
    user_query = input("请输入搜索关键词: ")
    web_search = WebSearch()
    results = web_search.search_and_filter(user_query)
    
    for result in results:
        print(f"标题: {result['title']}\n相关度: {result['score']}\n过滤后的内容: {result['filtered_content'][:500]}...\n")
