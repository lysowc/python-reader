from abc import ABC, abstractmethod
from util.log import Log
import validators
import requests
from io import BytesIO, BufferedReader
import random
import string
import os


class FileReadError(Exception):
    """文件读取相关错误"""

    pass


class ReaderBase(ABC):
    def __init__(self):
        self.logger = Log.channel(self.channel)
        self.file_stream = None

    @abstractmethod
    def read_bytes(self):
        """从字节流中读取内容，返回结构化数据"""
        pass

    def read(self, data):
        """
        读取文件内容，支持以下输入类型：
            - URL (字符串，以 http:// 或 https:// 开头)
            - 本地文件路径 (字符串，指向存在的文件)
            - 字节流 (BytesIO 或文件对象，如 open(..., 'rb') 返回的对象)

        参数：
            data: str (URL 或文件路径) 或 file-like object (支持 read() 的字节流)

        返回：
            结构化内容列表，如：
            [
                {"type": "text", "ext": ".txt", "data": "这里是文本"},
                {"type": "image", "ext": ".png", "data": "data:image/png;base64,..."},
                {"type": "table", "ext": ".table", "data": [["A1","B1"], ["A2","B2"]]}
            ]
        """
        try:
            # 情况1: 输入是 URL
            if isinstance(data, str) and validators.url(data):
                response = requests.get(data, timeout=30)
                response.raise_for_status()
                self.file_stream = BytesIO(response.content)
                self.file_stream.seek(0)

            # 情况2: 输入是字符串，且为本地路径
            elif isinstance(data, str) and os.path.exists(data):
                with open(data, "rb") as f:
                    content = f.read()
                self.file_stream = BytesIO(content)
                self.file_stream.seek(0)

            # 情况3: 输入是字节流对象（如 BytesIO 或 BufferedReader）
            elif hasattr(data, "read"):
                # 如果是 BytesIO 或类似对象
                if isinstance(data, BytesIO):
                    self.file_stream = data
                elif isinstance(data, BufferedReader):
                    # 是 open() 返回的文件句柄
                    pos = data.tell()
                    data.seek(0)
                    content = data.read()
                    data.seek(pos)  # 恢复原始位置（避免影响外部）
                    self.file_stream = BytesIO(content)
                else:
                    # 尝试通用 read()
                    pos = data.tell() if hasattr(data, "tell") else 0
                    if hasattr(data, "seek"):
                        data.seek(0)
                    content = data.read()
                    if hasattr(data, "seek"):
                        data.seek(pos)  # 尽量恢复位置
                    self.file_stream = BytesIO(content)
                self.file_stream.seek(0)

            else:
                return self.error(
                    message="输入类型不支持：请传入有效的 URL、本地文件路径,或可读的字节流对象"
                )
            # 调用统一的解析方法
            return self.read_bytes()

        except Exception as e:
            return self.error(message=f"文件处理失败: {str(e)}")

    def error(self, message: str):
        """
        抛出异常
        """
        raise FileReadError(message) from None

    def generate_random_string(self,length=16):
        """
        生成随机字符串
        """
        # 可选字符集：字母 + 数字
        characters = string.ascii_letters + string.digits  # abcdef...ABC...0123...
        return "".join(random.choices(characters, k=length))
