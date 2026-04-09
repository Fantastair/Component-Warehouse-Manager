""" 服务端部署脚本 """

import os
import sys
import venv
import shutil
import sqlite3
import subprocess
from pathlib import Path

from load_dotenv import load_env

CWD = Path(__file__).parent
DOT_ENV_PATH = CWD / ".env"

load_env(DOT_ENV_PATH)

print("欢迎使用[元件仓储管理器]服务端部署脚本")
print(
    "警告：本脚本只适用于服务端初次部署，请不要在已部署的环境中运行此脚本，"
    "否则可能会导致数据丢失。"
)
print("是否继续？(y/n)", end=" ")
choice = input().strip().lower()

if choice != "y":
    print("部署已取消。")
    sys.exit(0)

print("开始部署...")

print("创建运行环境...")
venv_path = CWD / ".venv"

if venv_path.exists():
    print(
        f"警告：已存在运行环境({venv_path})，可能不是初次部署，将重建运行环境，"
        "是否继续？(y/n)",
        end=" ",
    )
    choice = input().strip().lower()
    if choice != "y":
        print("部署已取消。")
        sys.exit(0)
    shutil.rmtree(venv_path)

venv.create(venv_path, with_pip=True)
if sys.platform == "win32":
    venv_path = venv_path / "Scripts" / "python.exe"
else:
    venv_path = venv_path / "bin" / "python"
print(f"运行环境已就绪: {venv_path}")

print("安装运行依赖...")
requirements = CWD / "requirements.txt"
if not requirements.exists():
    print(f"错误：未找到依赖文件({requirements})，请确保在正确的目录下运行此脚本。")
    sys.exit(1)
subprocess.run([venv_path, "-m", "pip", "install", "-r", requirements], check=True)
print("运行依赖已就绪")

print("初始化数据库...")
DB_PATH = CWD / "components.db"
if DB_PATH.exists():
    print(
        f"警告：已存在数据库文件({DB_PATH})，可能不是初次部署，将重建数据库，"
        "是否继续？(y/n)",
        end=" ",
    )
    choice = input().strip().lower()
    if choice != "y":
        print("部署已取消。")
        sys.exit(0)
    DB_PATH.unlink()

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute(
    """
CREATE TABLE categories (  -- 分类表
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 分类ID，自增主键
    name TEXT NOT NULL UNIQUE,  -- 分类名称，唯一且非空
    parent_id INTEGER,  -- 父分类ID，允许为空（顶级分类）
    remark TEXT,  -- 备注信息
    FOREIGN KEY (parent_id) REFERENCES categories(id)  -- 父分类ID外键关联categories表的id字段
);
"""
)

cursor.execute(
    """
CREATE TABLE components (  -- 元件表
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 组件ID，自增主键
    name TEXT NOT NULL,  -- 组件名称，非空
    category_id INTEGER,  -- 分类ID，外键关联categories表
    value TEXT,  -- 组件数值（如电阻的阻值、电容的电容值等）
    package TEXT,  -- 组件封装（如SMD、DIP等）
    lc_id TEXT,  -- 供应商料号
    location TEXT,  -- 存放位置
    remark TEXT,  -- 备注信息
    create_time TIMESTAMP DEFAULT (datetime('now','localtime')),  -- 创建时间，默认为当前时间
    FOREIGN KEY (category_id) REFERENCES categories(id)  -- 分类ID外键关联categories表的id字段
);
"""
)

cursor.execute(
    """
CREATE TABLE inventory (  -- 库存表
    component_id INTEGER PRIMARY KEY,  -- 物料ID，主键，外键关联components表的id字段
    quantity REAL NOT NULL DEFAULT 0,  -- 库存数量，非空，默认为0
    update_time TIMESTAMP DEFAULT (datetime('now','localtime')),  -- 更新时间，默认为当前时间
    FOREIGN KEY (component_id) REFERENCES components(id)  -- 物料ID外键关联components表的id字段
);
"""
)

cursor.execute(
    """
CREATE TABLE stock_records (  -- 库存变动记录表
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 记录ID，自增主键
    component_id INTEGER NOT NULL,  -- 物料ID，非空，外键关联components表的id字段
    type TEXT CHECK(type IN ('in', 'out')) NOT NULL,  -- 变动类型，入库'in'或出库'out'
    quantity REAL NOT NULL,  -- 变动数量，非空
    remark TEXT,  -- 备注信息
    create_time TIMESTAMP DEFAULT (datetime('now','localtime')),  -- 创建时间，默认为当前时间
    FOREIGN KEY (component_id) REFERENCES components(id)  -- 物料ID外键关联components表的id字段
);
"""
)

connection.commit()
connection.close()
print("数据库已就绪")

print("是否启动服务？(y/n)", end=" ")
choice = input().strip().lower()
if choice != "y":
    print("部署完成，但未启动服务。")
    sys.exit(0)

print("正在启动服务...")
APP_PATH = CWD / "app.py"
if not APP_PATH.exists():
    print(f"错误：未找到服务应用文件({APP_PATH})，请确保在正确的目录下运行此脚本。")
    sys.exit(1)

LOG_PATH = CWD / "server.log"

subprocess.Popen(  # pylint: disable=consider-using-with
    [venv_path, APP_PATH],
    start_new_session=True,
    stdout=LOG_PATH.open("w"),
    stderr=subprocess.STDOUT,
)
print(f"服务已启动，日志输出到: {LOG_PATH}")

HTTP_HOST = os.getenv("HTTP_HOST", "127.0.0.1")
HTTP_PORT = int(os.getenv("HTTP_PORT", "8000"))

print(
    f"[元件仓储管理器]服务端部署已完成，请访问 http://{HTTP_HOST}:{HTTP_PORT} 进行使用"
)
