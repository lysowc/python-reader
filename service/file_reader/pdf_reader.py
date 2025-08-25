from service.file_reader.base import ReaderBase
import fitz
import base64
from typing import List, Dict, Any


class PDFReader(ReaderBase):
    """
    PDF 文件读取器
    支持从文件流读取 .pdf 文件，提取文本、表格、图片(转为 base64)
    优化：过滤掉整行为空的表格行
    """

    channel: str = "pdf"

    def __init__(self):
        super().__init__()

    def read_bytes(self) -> List[List[Dict[str, Any]]]:
        """
        从文件流读取PDF内容并提取文本、表格和图片

        Returns:
            结构化内容列表，每页一个条目，每个条目包含该页的文本、表格和图片
        """
        content = []
        with fitz.open(stream=self.file_stream.read(), filetype="pdf") as doc:
            for page_num in range(len(doc)):
                page_data = self._process_page(doc, page_num)
                content += page_data

        return content

    def _process_page(self, doc: fitz.Document, page_num: int) -> List[Dict[str, Any]]:
        """处理单个页面的内容提取"""
        page = doc.load_page(page_num)
        page_data = []

        # 提取表格和其边界框
        tabs = page.find_tables()
        table_bboxes = [table.bbox for table in tabs.tables] if tabs.tables else []

        # 提取非表格文本
        text_blocks = page.get_text("blocks")
        for block in text_blocks:
            block_bbox = fitz.Rect(block[:4])
            is_inside_table = any(
                block_bbox.intersects(table_bbox) for table_bbox in table_bboxes
            )

            if not is_inside_table and block[4].strip():
                page_data.append({"type": "text", "ext": ".txt", "data": block[4]})

        # 提取表格并过滤空行
        if tabs.tables:
            for table in tabs.tables:
                table_data = table.extract()
                # 过滤掉整行为空的表格行
                filtered_table_data = [
                    row
                    for row in table_data
                    if any(cell and str(cell).strip() for cell in row)
                ]

                # 只有当表格有有效数据时才添加
                if filtered_table_data:
                    page_data.append(
                        {"type": "table", "ext": ".table", "data": filtered_table_data}
                    )

        # 提取图片
        self._extract_images(doc, page, page_data)

        return page_data

    def _extract_images(
        self, doc: fitz.Document, page: fitz.Page, page_data: List[Dict[str, Any]]
    ):
        """提取图片到页面数据"""
        images = page.get_images(full=True)
        if not images:
            return
        for img in images:
            base_image = doc.extract_image(img[0])
            if base_image:
                ext = base_image["ext"]
                img_data = base64.b64encode(base_image["image"]).decode("utf-8")
                page_data.append(
                    {
                        "type": "image",
                        "ext": ext,
                        "data": f"data:image/{ext};base64,{img_data}",
                    }
                )
