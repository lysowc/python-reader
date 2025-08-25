from abc import ABC, abstractmethod
from util.log import Log
import validators
import requests
from io import BytesIO

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
    
    def read(self, data:str):
        """
        读取文件内容
        参数：
            data: 文件路径 / URL(目前仅支持 URL)
        返回：
            结构化内容列表，如：
            [
                {"type": "text", "ext": ".txt", "data": "这里是文本"},
                {"type": "image", "ext": ".png", "data": "data:image/png;base64,..."},
                {"type": "table", "ext": ".table", "data": [["A1","B1"], ["A2","B2"]]}
            ]
        """
        if validators.url(data):
            try:
                response = requests.get(data, timeout=30)
                response.raise_for_status()
                self.file_stream = BytesIO(response.content)
                self.file_stream.seek(0)
                return self.read_bytes()
            except Exception as e:
                self.error(message=f"文件处理失败: {e}")
        else:
            self.error(message="暂不支持除 URL 以外的输入类型")
        
    def error(self, message: str):
        '''
        抛出异常
        '''
        raise FileReadError(message) from None
        
        
