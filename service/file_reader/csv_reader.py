from service.file_reader.base import ReaderBase
import csv
from io import TextIOWrapper


class CsvReader(ReaderBase):
    """
    日志渠道
    """

    channel: str = "csv"

    def __init__(self):
        super().__init__()

    def read_bytes(self):
        """
        从字节流读取
        """
        text_stream = TextIOWrapper(self.file_stream, encoding="utf-8", newline="")
        list_data = []
        try:
            reader = csv.reader(text_stream)
            for row in reader:
                # 去除空行：只要有一个字段非空（去空格后）就保留
                if any(cell.strip() for cell in row):
                    list_data.append(row)
        finally:
            text_stream.detach()  # 防止关闭 byte_stream

        # 按照与 Excel 一致的格式返回
        content = []
        if list_data:
            content.append({"type": "table", "ext": ".table", "data": list_data})
        return content
