""" 数据类定义 """

from dataclasses import dataclass


@dataclass
class CategoryItem:
    """分类数据模型"""

    id: int
    name: str
    parent_id: int | None
    remark: str | None
