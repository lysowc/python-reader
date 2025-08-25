from service.file_reader.base import ReaderBase
from docx import Document
from lxml import etree
import base64
import os
import re


class DocxReader(ReaderBase):
    """
    DOCX 文件读取器
    """

    channel: str = "docx"

    # 定义命名空间映射，避免重复定义
    NAMESPACES = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    }

    def __init__(self):
        super().__init__()

    def read_bytes(self):
        """
        从字节流读取DOCX文档内容,返回包含文本、图片和表格的数据列表
        """
        content = []
        docx = Document(self.file_stream)
        for element in docx.element.body:
            if element.tag.endswith("p"):
                # 处理段落中的图片
                if element.xpath(".//w:drawing"):
                    images = self._extract_image_from_element(element, docx)
                    content.extend(images)
                # 处理段落中的文本
                paragraph_text = self._extract_text_from_element(element)
                if paragraph_text:
                    content.append(
                        {"type": "text", "ext": ".txt", "data": paragraph_text}
                    )
            elif element.tag.endswith("tbl"):
                # 处理表格
                table_data = self._extract_table_data(element)
                if table_data:  # 只有当表格有数据时才添加
                    content.append(
                        {"type": "table", "ext": ".table", "data": table_data}
                    )
        return content

    def _extract_image_from_element(self, element, docx):
        """从元素中提取图片数据"""
        xml = etree.fromstring(element.xml)
        blips = xml.xpath(".//a:blip", namespaces=self.NAMESPACES)
        images = []
        for blip in blips:
            embed_id = blip.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
            )
            link_id = blip.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}link"
            )
            rId = embed_id or link_id
            if rId and rId in docx.part.rels:
                rel = docx.part.rels[rId]
                image_part = rel.target_part
                image_ext = os.path.splitext(image_part.partname)[1].lower()
                image_data = image_part.blob
                base64_data = base64.b64encode(image_data).decode("utf-8")
                # 确定MIME类型
                mime_type = (
                    f"image/{image_ext[1:]}"
                    if image_ext[1:] in ["jpeg", "jpg", "png", "gif", "bmp"]
                    else "image"
                )
                images.append(
                    {
                        "type": "image",
                        "ext": image_ext,
                        "data": f"data:{mime_type};base64,{base64_data}",
                    }
                )
        return images

    def _extract_text_from_element(self, element):
        """从元素中提取文本内容"""
        # 使用XPath提取所有文本节点
        xml = etree.fromstring(element.xml)
        text_nodes = xml.xpath(".//w:t/text()", namespaces=self.NAMESPACES)
        full_text = "".join(text_nodes).strip()

        # 清理多余的空白字符
        if full_text:
            full_text = re.sub(r"\s+", " ", full_text)

        return full_text

    def _extract_table_data(self, element):
        """提取表格数据，跳过全空行"""
        data = []
        for tr in element.findall(".//w:tr", self.NAMESPACES):
            row = []
            for tc in tr.findall(".//w:tc", self.NAMESPACES):
                texts = tc.findall(".//w:t", self.NAMESPACES)
                cell_text = "".join(t.text for t in texts if t.text is not None)
                row.append(cell_text.strip())
            # 检查是否整行都为空，如果不是则添加到数据中
            if any(cell for cell in row if cell):  # 至少有一个非空单元格
                data.append(row)
        return data
