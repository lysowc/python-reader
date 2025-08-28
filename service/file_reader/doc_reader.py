from service.file_reader.base import ReaderBase
from service.file_reader.docx_reader import DocxReader
import tempfile
import subprocess
import os
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import pathname2url
from io import BytesIO


class DocReader(ReaderBase):
    """
    日志渠道
    """

    channel: str = "doc"

    def __init__(self):
        super().__init__()

    def read_bytes(self):
        """
        从字节流读取
        """
        file = None
        with tempfile.TemporaryDirectory() as tmpdir:
            # 保存文件到临时文件夹
            file_name = self.generate_random_string() + ".doc"
            input_path = os.path.join(tmpdir, file_name)
            with open(input_path, "wb") as f:
                f.write(self.file_stream.read())
            tmp_path = Path(tmpdir).resolve()
            file_url = urljoin("file:", pathname2url(str(tmp_path)))
            command = [
                # r"C:\Program Files\LibreOffice\program\soffice.exe",
                "soffice",
                f"-env:UserInstallation={file_url}",
                "--headless",
                "--convert-to",
                "docx",
                input_path,
                "--outdir",
                tmpdir,
            ]
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            if result.returncode != 0:
                raise Exception(f"转换失败: {result.stderr}")

            # 构造输出路径（soffice 使用原文件名）
            stem = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(tmpdir, f"{stem}.docx")
            if not os.path.exists(output_path):
                raise Exception("转换后文件未生成")
            with open(output_path, "rb") as f:
                file = f.read()
            file = BytesIO(file)
        reader = DocxReader()
        return reader.read(file)
