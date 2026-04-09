""" 服务端解除部署脚本 """

import os
import sys
import shutil
from pathlib import Path

from load_dotenv import load_env

CWD = Path(__file__).parent
DOT_ENV_PATH = CWD / ".env"

load_env(DOT_ENV_PATH)

HTTP_PORT = int(os.getenv("HTTP_PORT", "8000"))

print("欢迎使用[元件仓储管理器]服务端解除部署脚本")
print("警告：本脚本将删除服务端的运行环境和数据库文件，请确保已备份重要数据。")
print("是否继续？(y/n)", end=" ")
choice = input().strip().lower()
if choice != "y":
    print("解除部署已取消。")
    sys.exit(0)

print("开始解除部署...")

print("关停服务...")
os.system(
    f"lsof -i :{HTTP_PORT} | grep python | awk '{{print $2}}' | xargs kill -9 2>/dev/null"
)
print("服务已关闭")

print("是否继续清理部署文件？(y/n)", end=" ")
choice = input().strip().lower()
if choice != "y":
    print("解除部署已完成，但部署文件未清理。")
    print("如果需要，请手动删除部署目录下的文件以彻底清理。")
    sys.exit(0)

print("清理日志文件...")
LOG_PATH = CWD / "server.log"
if LOG_PATH.exists():
    os.remove(LOG_PATH)
    print("日志文件已删除")
else:
    print("未找到日志文件，无需删除")

print("删除数据库文件...")
db_path = CWD / "components.db"
if db_path.exists():
    db_path.unlink()
    print("数据库文件已删除")
else:
    print("未找到数据库文件，无需删除")

print("删除运行环境...")
venv_path = CWD / ".venv"
if venv_path.exists():
    shutil.rmtree(venv_path)
    print("运行环境已删除")
else:
    print("未找到运行环境，无需删除")

print("解除部署已完成")
print("如果需要，请手动删除部署目录下的其他文件以彻底清理")
print("如果需要重新部署，请运行 deploy.py 脚本进行部署")
