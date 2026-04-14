""" 数据类定义 """

from pydantic import BaseModel


class CategoryItem(BaseModel):
    """分类数据模型"""

    id: int
    name: str
    parent_id: int | None = None
    remark: str | None = None
