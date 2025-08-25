from service.file_reader.base import ReaderBase
import xlrd


class XlsReader(ReaderBase):
    """
    日志渠道
    """

    channel: str = "xls"

    def __init__(self):
        super().__init__()

    def read_bytes(self):
        """
        从字节流读取
        """
        wb = xlrd.open_workbook(file_contents=self.file_stream.read())
        # 获取表格所有 sheet 名称
        content = []
        sheets = wb.sheet_names()
        for sheet in sheets:
            worksheet = wb[sheet]
            list_data = []
            for row in worksheet.get_rows():
                tmp = []
                for cell in row:
                    tmp.append(cell.value)
                list_data.append(tmp)
            if list_data:
                content.append({"type": "table", "ext": ".table", "data": list_data})
        return content
