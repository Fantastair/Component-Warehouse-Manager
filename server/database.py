""" 数据库管理脚本 """

import sqlite3
from pathlib import Path

from data_class import CategoryItem

CWD = Path(__file__).parent


class Database:
    """数据库管理类"""

    def __init__(self, db_file: Path):
        """初始化数据库管理器"""
        self.db_file = db_file
        self.conn: sqlite3.Connection
        self.cursor: sqlite3.Cursor

    def __enter__(self) -> "Database":
        """进入上下文管理器，连接数据库"""
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器，断开数据库连接"""
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def get_categories(self) -> list[CategoryItem]:
        """获取所有分类"""
        with self:
            self.cursor.execute("SELECT id, name, parent_id, remark FROM categories")
            rows = self.cursor.fetchall()
            return [CategoryItem(*row) for row in rows]
