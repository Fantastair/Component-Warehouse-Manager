""" 服务器应用，提供API接口供前端调用 """

import os
from pathlib import Path

import dotenv
import uvicorn
import fastapi
from fastapi import Header, HTTPException

from database import Database

CWD = Path(__file__).parent
DOT_ENV_PATH = CWD / ".env"
dotenv.load_dotenv(DOT_ENV_PATH)

HTTP_HOST = os.getenv("HTTP_HOST", "http://127.0.0.1")
HTTP_PORT = int(os.getenv("HTTP_PORT", "8000"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
PROCESS_WORKERS = int(os.getenv("PROCESS_WORKERS", "4"))
API_TOKEN = os.getenv("API_TOKEN")
if API_TOKEN is None:
    print("警告：未设置API_TOKEN环境变量，接口访问将不受保护！")


def verify_token(token: str) -> bool:
    """验证API令牌"""
    return token == API_TOKEN


app = fastapi.FastAPI(root_path="/cwm/api/v1")


@app.post("/verify-token")
def api_verify_token(authorization: str = Header(None)) -> dict[str, str]:
    """验证令牌"""
    if API_TOKEN is None:
        return {"detail": "未设置令牌，接口访问不受保护"}
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供令牌")
    try:
        token_type, token = authorization.split()
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="令牌类型错误")
    except ValueError as e:
        raise HTTPException(status_code=401, detail="令牌格式错误") from e
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="无效的令牌")
    return {"detail": "令牌验证成功"}


if __name__ == "__main__":
    if ENVIRONMENT == "dev":
        print("正在以开发模式启动服务...")
        uvicorn.run(
            "app:app",
            host=HTTP_HOST,
            port=HTTP_PORT,
            reload=True,
            log_level="debug",
        )
    else:
        print("正在以生产模式启动服务...")
        uvicorn.run(
            "app:app",
            host=HTTP_HOST,
            port=HTTP_PORT,
            workers=PROCESS_WORKERS,
            reload=False,
            log_level="info",
        )
else:
    DB = Database(CWD / "components.db")
    DB.connect()
