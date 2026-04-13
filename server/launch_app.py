""" 后端服务启动脚本 """

import os
from pathlib import Path

import dotenv
import uvicorn


def main() -> None:
    """启动服务"""
    cwd = Path(__file__).parent
    dot_env_path = cwd / ".env"
    dotenv.load_dotenv(dot_env_path)

    http_host = os.getenv("HTTP_HOST", "http://127.0.0.1")
    http_port = int(os.getenv("HTTP_PORT", "8000"))
    environment = os.getenv("ENVIRONMENT", "dev")
    process_workers = int(os.getenv("PROCESS_WORKERS", "4"))

    if environment == "dev":
        print("正在以开发模式启动服务...")
        uvicorn.run(
            "app:app",
            host=http_host.split("://")[-1],
            port=http_port,
            reload=True,
            log_level="debug",
        )
    else:
        print("正在以生产模式启动服务...")
        uvicorn.run(
            "app:app",
            host=http_host.split("://")[-1],
            port=http_port,
            workers=process_workers,
            reload=False,
            log_level="info",
        )


if __name__ == "__main__":
    main()
