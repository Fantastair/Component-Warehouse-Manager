""" 服务器应用，提供API接口供前端调用 """

import os
from pathlib import Path

import dotenv
import fastapi
from pydantic import BaseModel
from fastapi import Header, APIRouter, HTTPException

from database import Database
from data_class import CategoryItem

CWD = Path(__file__).parent
DOT_ENV_PATH = CWD / ".env"
dotenv.load_dotenv(DOT_ENV_PATH)

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
API_TOKEN = os.getenv("API_TOKEN")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

if API_TOKEN is None:
    print("警告：未设置API_TOKEN环境变量，接口访问将不受保护！")


def verify_token(authorization: str) -> bool:
    """验证API令牌"""
    if API_TOKEN is None:
        return True
    if not authorization:
        return False
    try:
        token_type, token = authorization.split()
        if token_type.lower() != "bearer":
            return False
    except ValueError:
        return False
    return token == API_TOKEN


app = fastapi.FastAPI(
    root_path="/cwm/api/v1",
    debug=(ENVIRONMENT == "dev"),
    title="Fantas元件仓储管理器",
    description="提供元件仓储管理的后端API接口",
    version="1.0.0.dev1",
)
DB = Database(CWD / "components.db")


class DetailResponse(BaseModel):
    """通用详情响应模型"""

    detail: str


@app.post("/verify-token", tags=["身份认证"])
def api_verify_token(authorization: str = Header(None)) -> DetailResponse:
    """验证令牌"""
    if verify_token(authorization):
        return DetailResponse(detail="令牌验证成功")
    raise HTTPException(status_code=401, detail="令牌验证失败")


# ==================== 分类表相关接口 ====================

category_router = APIRouter(prefix="/categories", tags=["分类管理"])


@category_router.get("")
def api_get_categories(
    authorization: str = Header(None),
) -> list[CategoryItem]:
    """获取所有分类"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    return DB.get_categories()


@category_router.get("/paged")
def api_get_categories_paged(
    page: int, page_size: int, authorization: str = Header(None)
) -> list[CategoryItem]:
    """获取分页分类列表"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    return DB.get_categories_paged(page, page_size)


@category_router.get("/id/{category_id}")
def api_get_category_by_id(
    category_id: int, authorization: str = Header(None)
) -> CategoryItem:
    """根据ID获取分类"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    category = DB.get_category_by_id(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="分类未找到")
    return category


class CategoryExistsResponse(BaseModel):
    """分类存在检查响应模型"""

    exists: bool


@category_router.get("/exists")
def api_check_category_exists(
    category_id: int, authorization: str = Header(None)
) -> CategoryExistsResponse:
    """检查分类是否存在"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    exists = DB.is_category_exists(category_id)
    return CategoryExistsResponse(exists=exists)


@category_router.get("/name/{name}")
def api_get_categories_by_name(
    name: str, authorization: str = Header(None)
) -> CategoryItem:
    """根据名称获取分类"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    category = DB.get_categories_by_name(name)
    if category is None:
        raise HTTPException(status_code=404, detail="分类未找到")
    return category


@category_router.get("/search")
def api_search_categories_by_name(
    name: str, authorization: str = Header(None)
) -> list[CategoryItem]:
    """根据名称模糊搜索分类"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    return DB.search_categories_by_name(name)


@category_router.get("/parent")
def api_get_all_parent_categories(
    category_id: int, authorization: str = Header(None)
) -> list[CategoryItem]:
    """获取指定分类的所有父级分类直至根分类"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    return DB.get_all_parent_categories(category_id)


@category_router.get("/child")
def api_get_all_child_categories(
    category_id: int, authorization: str = Header(None)
) -> list[CategoryItem]:
    """获取指定分类的所有子分类（不递归展开）"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    return DB.get_all_child_categories(category_id)


class AddCategoryResponse(BaseModel):
    """添加分类响应模型"""

    id: int


@category_router.post("/add")
def api_add_category(
    category: CategoryItem, authorization: str = Header(None)
) -> AddCategoryResponse:
    """
    添加分类

    id 字段会被忽略，接口会自动生成新分类ID并返回
    """
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    try:
        new_id = DB.add_category(category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return AddCategoryResponse(id=new_id)


@category_router.post("/update")
def api_update_category(
    category: CategoryItem, authorization: str = Header(None)
) -> DetailResponse:
    """更新分类"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    # if not DB.is_category_exists(category.id):
        # raise HTTPException(status_code=404, detail="分类未找到")
    DB.update_category(category)
    return DetailResponse(detail="分类更新成功")


@category_router.post("/delete")
def api_delete_category(
    category_id: int, authorization: str = Header(None)
) -> DetailResponse:
    """删除分类"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    if not DB.is_category_exists(category_id):
        raise HTTPException(status_code=404, detail="分类未找到")
    DB.delete_category(category_id)
    return DetailResponse(detail="分类删除成功")


# 添加路由
app.include_router(category_router)
