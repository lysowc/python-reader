from service.file_reader.base import ReaderBase
from PIL import Image
import io
from openpyxl import load_workbook
import base64


class XlsxReader(ReaderBase):
    """
    日志渠道
    """

    channel: str = "xlsx"

    def __init__(self):
        super().__init__()

    def read_bytes(self):
        """
        从字节流读取
        """
        content = []
        # 读取内容
        wb = load_workbook(filename=self.file_stream)
        content = []
        # 获取表格所有 sheet 名称
        sheets = wb.sheetnames
        for sheet in sheets:
            worksheet = wb[sheet]
            # 读取单元格数据
            list_data = []
            for row in worksheet.iter_rows(values_only=True):
                list_data.append(list(row))
            if list_data:
                content.append({"type": "table", "ext": ".table", "data": list_data})
            for idx, image in enumerate(worksheet._images, 1):
                image_data = image._data()
                # 使用Pillow读取图片信息
                img = Image.open(io.BytesIO(image_data))
                image_ext = img.format.lower()  # 获取格式并转为小写
                img_data = base64.b64encode(image_data).decode("utf-8")
                content.append(
                    {
                        "type": "image",
                        "ext": image_ext,
                        "data": f"data:image/{image_ext};base64,{img_data}",
                    }
                )
        return content
