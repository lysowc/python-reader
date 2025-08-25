from service.file_reader.base import ReaderBase


class TxtReader(ReaderBase):
    """
    日志渠道
    """

    channel: str = "txt"

    def __init__(self):
        super().__init__()

    def read_bytes(self):
        """
        从字节流读取
        """
        content = []
        # 读取文本内容
        text = self.file_stream.read().decode("utf-8")
        lines = text.splitlines()
        for line in lines:
            stripped = line.strip()
            content.append({"type": "text", "ext": ".txt", "data": stripped})
        return content
