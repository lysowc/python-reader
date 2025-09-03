from fastapi import APIRouter
from schema.embedding import EmbeddingParam, EmbeddingResponse
from schema.api import ApiResponse
from util.response import returnJson
from util.embedding import embedding

router = APIRouter(prefix="/embedding")

@router.post("/query", response_model=ApiResponse[EmbeddingResponse])
def generate_embedding(query: EmbeddingParam):
    # 修改函数名为generate_embedding，更符合实际功能
    return returnJson(data=embedding(query.query))