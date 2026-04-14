""" 数据类定义 """

from dataclasses import dataclass


@dataclass(slots=True)
class CategoryItem:
    """分类数据模型"""

    id: int
    name: str
    parent_id: int | None = None
    remark: str | None = None
