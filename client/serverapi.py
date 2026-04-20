""" 客户端与服务器交互的模块，封装了API调用逻辑 """

import os
import json
from dataclasses import asdict

import httpx
import dotenv

from data_class import CategoryItem

dotenv.load_dotenv()

HTTP_HOST = os.getenv("HTTP_HOST", "http://127.0.0.1")
HTTP_PORT = int(os.getenv("HTTP_PORT", "8000"))
API_TOKEN = os.getenv("API_TOKEN")

BASE_URL = ""  # API基础URL，登录后会根据输入的服务器地址和端口设置
HEADERS: dict[str, str] = {}  # 全局请求头，登录后会设置Authorization字段


# ==================== 身份认证 ====================


async def verify_token(host: str, port: str, api_token: str) -> bool:
    """验证API令牌"""
    global HEADERS, BASE_URL

    BASE_URL = f"{host}:{port}/cwm/api/v1"
    HEADERS = {"Authorization": f"Bearer {api_token}"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/verify-token", headers=HEADERS, timeout=5
            )
        if response.status_code == 200:
            return True
        print(response.json())
        return False
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return False


# ==================== 分类表相关API ====================


async def get_categories() -> list[CategoryItem] | None:
    """获取所有分类"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/categories", headers=HEADERS, timeout=5
            )
        if response.status_code == 200:
            return [CategoryItem(**item) for item in response.json()]
        print(f"获取分类失败: {response.status_code} - {response.json()}")
        return None
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return None


async def get_categories_paged(page: int, page_size: int) -> list[CategoryItem] | None:
    """获取分页分类列表"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/categories/paged",
                headers=HEADERS,
                params={"page": page, "page_size": page_size},
                timeout=5,
            )
        if response.status_code == 200:
            return [CategoryItem(**item) for item in response.json()]
        print(f"获取分页分类失败: {response.status_code} - {response.json()}")
        return None
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return None


async def get_category_by_id(category_id: int) -> CategoryItem | None:
    """根据ID获取分类"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/categories/id/{category_id}", headers=HEADERS, timeout=5
            )
        if response.status_code == 200:
            return CategoryItem(**response.json())
        print(f"获取分类失败: {response.status_code} - {response.json()}")
        return None
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return None


async def is_category_exists(category_id: int) -> bool | None:
    """检查分类是否存在"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/categories/exists",
                headers=HEADERS,
                params={"category_id": category_id},
                timeout=5,
            )
        if response.status_code == 200:
            return response.json().get("exists", False)  # type: ignore[no-any-return]
        print(f"检查分类存在失败: {response.status_code} - {response.json()}")
        return None
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return None


async def get_categories_by_name(name: str) -> CategoryItem | None:
    """根据名称获取分类"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/categories/name/{name}", headers=HEADERS, timeout=5
            )
        if response.status_code == 200:
            return CategoryItem(**response.json())
        print(f"获取分类失败: {response.status_code} - {response.json()}")
        return None
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return None


async def search_categories_by_name(name: str) -> list[CategoryItem] | None:
    """根据名称获取分类列表"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/categories/search",
                headers=HEADERS,
                params={"name": name},
                timeout=5,
            )
        if response.status_code == 200:
            return [CategoryItem(**item) for item in response.json()]
        print(f"获取分类失败: {response.status_code} - {response.json()}")
        return None
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return None


async def get_all_parent_categories(category_id: int) -> list[CategoryItem] | None:
    """获取指定分类的所有父级分类直至根分类"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/categories/parent",
                headers=HEADERS,
                params={"category_id": category_id},
                timeout=5,
            )
        if response.status_code == 200:
            return [CategoryItem(**item) for item in response.json()]
        print(f"获取父级分类失败: {response.status_code} - {response.json()}")
        return None
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return None


async def get_all_child_categories(category_id: int) -> list[CategoryItem] | None:
    """获取指定分类的所有子分类（不递归展开）"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/categories/child",
                headers=HEADERS,
                params={"category_id": category_id},
                timeout=5,
            )
        if response.status_code == 200:
            return [CategoryItem(**item) for item in response.json()]
        print(f"获取子级分类失败: {response.status_code} - {response.json()}")
        return None
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return None


async def add_category(
    name: str, parent: int | str | None = None, remark: str | None = None
) -> int | None:
    """
    添加分类，返回新分类ID

    parent 参数可以是 int 类型作为父分类 ID，也可以是 str 类型作为父分类名称
    仅当字符串精准匹配到一个分类时才会使用该分类作为父分类，否则视为无父分类
    """
    if isinstance(parent, str):
        parent_categories = await get_categories_by_name(parent)
        parent_id = parent_categories.id if parent_categories is not None else None
    else:
        parent_id = parent
    category = CategoryItem(
        id=0,
        name=name,
        parent_id=parent_id,
        remark=remark,
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/categories/add",
                headers=HEADERS,
                json=asdict(category),
                timeout=5,
            )
        if response.status_code == 200:
            return response.json().get("id")  # type: ignore[no-any-return]
        print(f"添加分类失败: {response.status_code} - {response.json()}")
        return None
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return None


async def update_category(
    category: int | str,
    name: str | None = None,
    parent: int | str | None = None,
    remark: str | None = None,
    update_parent: bool = False,
    update_remark: bool = False,
) -> bool:
    """
    更新分类

    category 参数可以是 int 类型作为分类 ID，也可以是 str 类型作为分类名称
    仅当字符串精准匹配到一个分类时才会更新该分类，否则返回 False

    parent 参数可以是 int 类型作为父分类 ID，也可以是 str 类型作为父分类名称
    仅当字符串精准匹配到一个分类时才会使用该分类作为父分类，否则视为无父分类

    name、parent、remark 参数如果为 None 则不更新对应字段
    update_parent 和 update_remark 参数为 True 时可以以将 parent 和 remark 字段更新为 None
    """
    if isinstance(category, str):
        category_item = await get_categories_by_name(category)
        if category_item is None:
            print(f"未找到分类: {category_item}")
            return False
    else:
        category_item = await get_category_by_id(category)
        if category_item is None:
            print(f"未找到分类: {category_item}")
            return False

    if name is not None:
        category_item.name = name

    if parent is not None:
        if isinstance(parent, str):
            parent_categories = await get_categories_by_name(parent)
            category_item.parent_id = (
                parent_categories.id if parent_categories is not None else None
            )
        else:
            category_item.parent_id = parent
    elif update_parent:
        category_item.parent_id = None

    if remark is not None:
        category_item.remark = remark
    elif update_remark:
        category_item.remark = None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/categories/update",
                headers=HEADERS,
                json=asdict(category_item),
                timeout=5,
            )
        if response.status_code == 200:
            return True
        print(f"更新分类失败: {response.status_code} - {response.json()}")
        return False
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return False


async def delete_category(category: int | str) -> bool:
    """
    删除分类

    category 参数可以是 int 类型作为分类 ID，也可以是 str 类型作为分类名称
    仅当字符串精准匹配到一个分类时才会删除该分类，否则返回 False
    """
    if isinstance(category, str):
        category_item = await get_categories_by_name(category)
        if category_item is None:
            print(f"未找到分类: {category_item}")
            return False
        category_id = category_item.id
    else:
        category_id = category

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/categories/delete",
                headers=HEADERS,
                params={"category_id": category_id},
                timeout=5,
            )
        if response.status_code == 200:
            return True
        print(f"删除分类失败: {response.status_code} - {response.json()}")
        return False
    except (httpx.HTTPError, json.decoder.JSONDecodeError) as e:
        print(f"请求异常: {e}")
        return False
