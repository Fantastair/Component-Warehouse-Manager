""" 客户端与服务器交互的模块，封装了API调用逻辑 """
import os

import dotenv
import requests

dotenv.load_dotenv()

HTTP_HOST = os.getenv("HTTP_HOST", "127.0.0.1")
HTTP_PORT = int(os.getenv("HTTP_PORT", "8000"))
API_TOKEN = os.getenv("API_TOKEN")

BASE_URL = f"http://{HTTP_HOST}:{HTTP_PORT}/cwm/api/v1"

def verify_token() -> bool:
    """ 验证API令牌 """
    if not API_TOKEN:
        return False

    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    try:
        response = requests.post(f"{BASE_URL}/verify-token", headers=headers, timeout=10)
        if response.status_code == 200:
            print(response.json().get("detail"))
            return True
        else:
            print(f"令牌验证失败: {response.status_code} - {response.json()}")
            return False
    except requests.RequestException as e:
        print(f"请求异常: {e}")
        return False
