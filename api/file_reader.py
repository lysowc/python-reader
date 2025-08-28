from fastapi import APIRouter
from schema.file_reader import FileReader, FileContent
from schema.api import ApiResponse
from util.response import returnJson
from typing import List
from service.file_reader.doc_reader import DocReader
from service.file_reader.docx_reader import DocxReader
from service.file_reader.pdf_reader import PDFReader
from service.file_reader.txt_reader import TxtReader
from service.file_reader.xls_reader import XlsReader
from service.file_reader.xlsx_reader import XlsxReader

router = APIRouter(prefix="/files", tags=["file"])


@router.post("/read", response_model=ApiResponse[List[FileContent]])
def read_file(files: List[FileReader]):
    readers = {
        "doc": DocReader,
        "docx": DocxReader,
        "pdf": PDFReader,
        "txt": TxtReader,
        "xls": XlsReader,
        "xlsx": XlsxReader,
    }

    result = []
    for file in files:
        ext = file.ext.lower()
        if ext in readers:
            reader = readers[ext]()
            try:
                content = reader.read(file.content)
                result.extend(content)
            except Exception as e:
                # 处理读取错误
                return returnJson(code=400, message=f"读取失败: {e}")
        else:
            return returnJson(code=400, message=f"暂不支持的文件类型{ext}")

    return returnJson(data=result)
