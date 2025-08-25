from pydantic import BaseModel

"""
文件读取接口参数
@param content: 文件内容
@param ext: 文件扩展名
"""
class FileReader(BaseModel):
    content: str
    ext: str
    
    class Config:
        extra = "allow"  # 允许额外字段

"""
返回文件数据
@param type: 类型 image,table,text
@param ext: 后缀 txt,table,image 
@param data: 内容
"""
class FileContent(BaseModel):
    type: str
    ext: str
    data: str