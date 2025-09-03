from pydantic import BaseModel
from typing import List

"""
请求参数
@param query: 要向量化的内容
"""


class EmbeddingParam(BaseModel):
    query: str

    class Config:
        extra = "allow"  # 允许额外字段


"""
返回向量化数据
@param data: 内容
"""


class EmbeddingResponse(BaseModel):
    data: List[float]