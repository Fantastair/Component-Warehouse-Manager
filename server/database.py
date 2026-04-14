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

    def __exit__(self, *_) -> None:  # type: ignore[no-untyped-def]
        """退出上下文管理器，断开数据库连接"""
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    # ==================== 分类表相关操作 ====================

    def get_categories(self) -> list[CategoryItem]:
        """获取所有分类"""
        with self:
            self.cursor.row_factory = sqlite3.Row
            self.cursor.execute("SELECT id, name, parent_id, remark FROM categories")
            rows = self.cursor.fetchall()
            return [CategoryItem(**row) for row in rows]

    def get_categories_paged(self, page: int, page_size: int) -> list[CategoryItem]:
        """获取分页分类列表"""
        offset = page * page_size
        with self:
            self.cursor.row_factory = sqlite3.Row
            self.cursor.execute(
                "SELECT id, name, parent_id, remark FROM categories LIMIT ? OFFSET ?",
                (page_size, offset),
            )
            rows = self.cursor.fetchall()
            return [CategoryItem(**row) for row in rows]

    def get_category_by_id(self, category_id: int) -> CategoryItem | None:
        """根据ID获取分类"""
        with self:
            self.cursor.row_factory = sqlite3.Row
            self.cursor.execute(
                "SELECT id, name, parent_id, remark FROM categories WHERE id = ?",
                (category_id,),
            )
            row = self.cursor.fetchone()
            if row is not None:
                return CategoryItem(**row)
            return None

    def is_category_exists(self, category_id: int) -> bool:
        """检查分类是否存在"""
        with self:
            self.cursor.execute("SELECT 1 FROM categories WHERE id = ?", (category_id,))
            return self.cursor.fetchone() is not None

    def get_categories_by_name(self, name: str) -> list[CategoryItem]:
        """根据名称模糊搜索分类"""
        with self:
            self.cursor.row_factory = sqlite3.Row
            self.cursor.execute(
                "SELECT id, name, parent_id, remark FROM categories WHERE name LIKE ?",
                (f"%{name}%",),
            )
            rows = self.cursor.fetchall()
            return [CategoryItem(**row) for row in rows]

    def get_all_parent_categories(self, category_id: int) -> list[CategoryItem]:
        """获取指定分类的所有父级分类直至根分类"""
        parents = []
        current_id = category_id
        while True:
            category = self.get_category_by_id(current_id)
            if category is None or category.parent_id is None:
                break
            parent_category = self.get_category_by_id(category.parent_id)
            if parent_category is not None:
                parents.append(parent_category)
                current_id = parent_category.id
            else:
                break
        return parents

    def get_all_child_categories(self, category_id: int) -> list[CategoryItem]:
        """获取指定分类的所有子级分类（不递归展开）"""
        with self:
            self.cursor.row_factory = sqlite3.Row
            self.cursor.execute(
                "SELECT id, name, parent_id, remark FROM categories WHERE parent_id = ?",
                (category_id,),
            )
            rows = self.cursor.fetchall()
            return [CategoryItem(**row) for row in rows]

    def add_category(self, category: CategoryItem) -> int:
        """添加分类，返回新分类ID"""
        with self:
            try:
                self.cursor.execute(
                    "INSERT INTO categories (name, parent_id, remark) VALUES (?, ?, ?)",
                    (category.name, category.parent_id, category.remark),
                )
            except sqlite3.IntegrityError as e:
                raise ValueError(f"分类名不能重复: {e}")
            self.conn.commit()
            if self.cursor.lastrowid is not None:
                return self.cursor.lastrowid
            raise RuntimeError("未能获取新分类ID，可能是由于插入失败导致的")

    def update_category(self, category: CategoryItem) -> None:
        """更新分类"""
        with self:
            self.cursor.execute(
                "UPDATE categories SET name = ?, parent_id = ?, remark = ? WHERE id = ?",
                (category.name, category.parent_id, category.remark, category.id),
            )
            self.conn.commit()

    def delete_category(self, category_id: int) -> None:
        """删除分类"""
        with self:
            self.cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            self.conn.commit()
