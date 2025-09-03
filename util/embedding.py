import torch
from sentence_transformers import SentenceTransformer
import numpy as np
from config.embedding import EmbeddingSettings

# 读取配置
embedding_settings = EmbeddingSettings()

# 自动选择设备
if torch.cuda.is_available():
    # 多 GPU 场景：轮询分配 worker 到不同 GPU
    try:
        import os

        n_gpu = torch.cuda.device_count()
        gpu_id = os.getpid() % n_gpu
        device = f"cuda:{gpu_id}"
    except Exception as e:
        device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"  # Apple Silicon GPU
else:
    device = "cpu"

model = SentenceTransformer(embedding_settings.EMBEDDING_MODEL_PATH, device=device)


def embedding(text: str):
    """
    生成嵌入后的向量 -- 已经归一化
    """
    # 生成嵌入
    embedding = model.encode([text])[0]  # 得到 numpy 数组
    embedding_normalized = embedding / np.linalg.norm(embedding)
    return embedding_normalized.tolist()
