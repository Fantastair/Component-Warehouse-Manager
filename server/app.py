""" 服务器应用，提供API接口供前端调用 """

import os
import atexit
from typing import Any
from pathlib import Path

import dotenv
import fastapi
from fastapi import Header, HTTPException

import database
from database import Database

CWD = Path(__file__).parent
DOT_ENV_PATH = CWD / ".env"
dotenv.load_dotenv(DOT_ENV_PATH)

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
API_TOKEN = os.getenv("API_TOKEN")

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


app = fastapi.FastAPI(root_path="/cwm/api/v1")


@app.post("/verify-token")
def api_verify_token(authorization: str = Header(None)) -> dict[str, Any]:
    """验证令牌"""
    if verify_token(authorization):
        return {"status_code": 200, "message": "令牌验证成功"}
    return {"status_code": 401, "message": "令牌验证失败"}


@app.get("/categories")
def api_get_categories(
    authorization: str = Header(None),
) -> list[database.CategoryItem]:
    """获取所有分类"""
    if not verify_token(authorization):
        raise HTTPException(status_code=401, detail="令牌验证失败")
    try:
        categories = DB.get_categories()
        return categories
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="获取分类失败") from e


DB = Database(CWD / "components.db")
DB.connect()

atexit.register(DB.disconnect)
