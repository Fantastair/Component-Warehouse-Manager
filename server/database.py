""" 数据库管理脚本 """

import sqlite3
from pathlib import Path

CWD = Path(__file__).parent


class Database:
    """数据库管理类"""

    def __init__(self, db_file: Path):
        """初始化数据库管理器"""
        self.db_file = db_file
        self.connection: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def connect(self) -> None:
        """连接数据库"""
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def disconnect(self) -> None:
        """断开数据库连接"""
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.connection is not None:
            self.connection.close()
            self.connection = None
