""" 客户端与服务器交互的模块，封装了API调用逻辑 """

import os
import uuid
import threading
from queue import Queue
from typing import Any, Callable

import dotenv
import requests

import fantas

from data_class import CategoryItem

dotenv.load_dotenv()

HTTP_HOST = os.getenv("HTTP_HOST", "http://127.0.0.1")
HTTP_PORT = int(os.getenv("HTTP_PORT", "8000"))
API_TOKEN = os.getenv("API_TOKEN")

BASE_URL = f"{HTTP_HOST}:{HTTP_PORT}/cwm/api/v1"

GET_API_RESPONSE = fantas.custom_event()

requests_queue: Queue = Queue()  # 请求队列

headers = {"Authorization": f"Bearer {API_TOKEN}"}  # 通用请求头


def api_request(method: Callable, *args: tuple, **kwargs: dict) -> int:
    """非阻塞的API请求函数"""
    uid = uuid.uuid4().int
    requests_queue.put((method, uid, args, kwargs))
    return uid


def process_api_request(
    method: Callable, uid: int, *args: tuple, **kwargs: dict
) -> None:
    """处理API请求，调用方法并处理结果"""
    try:
        result: Any = method(*args, **kwargs)
        event: fantas.Event = fantas.Event(
            GET_API_RESPONSE, {"uid": uid, "result": result}
        )
        fantas.event.post(event)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"请求 {uid} 失败: {e}")


def api_worker() -> None:
    """API请求工作线程，处理请求队列中的请求"""
    while True:
        method, uid, args, kwargs = requests_queue.get()
        t = threading.Thread(
            target=process_api_request, args=(method, uid) + args, kwargs=kwargs
        )
        t.daemon = True
        t.start()


api_worker_thread = threading.Thread(target=api_worker)
api_worker_thread.daemon = True
api_worker_thread.start()


def verify_token() -> bool:
    """验证API令牌"""
    if not API_TOKEN:
        return False

    try:
        response = requests.post(
            f"{BASE_URL}/verify-token", headers=headers, timeout=10
        )
        if response.status_code == 200:
            return True
        print(response.json())
        return False
    except requests.RequestException as e:
        print(f"请求异常: {e}")
        return False


def get_categories() -> list[CategoryItem]:
    """获取所有分类"""
    try:
        response = requests.get(f"{BASE_URL}/categories", headers=headers, timeout=10)
        if response.status_code == 200:
            return [CategoryItem(**item) for item in response.json()]
        print(f"获取分类失败: {response.status_code} - {response.json()}")
        return None
    except requests.RequestException as e:
        print(f"请求异常: {e}")
        return None
