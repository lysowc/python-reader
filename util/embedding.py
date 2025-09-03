import torch
from sentence_transformers import SentenceTransformer
import numpy as np
from config.embedding import EmbeddingSettings

# 读取配置
embedding_settings = EmbeddingSettings()

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available() else "cpu"
)
model = SentenceTransformer(
    embedding_settings.EMBEDDING_MODEL_PATH, device=device
)


def embedding(text: str):
    """
    生成嵌入后的向量 -- 已经归一化
    """
    # 生成嵌入
    embedding = model.encode([text])[0]  # 得到 numpy 数组
    embedding_normalized = embedding / np.linalg.norm(embedding)
    return embedding_normalized.tolist()
