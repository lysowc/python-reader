from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def returnJson(data=None, message="Success", code=200, status_code=200):
    '''
    返回Json数据
    '''
    res = jsonable_encoder(data)
    return JSONResponse(
        status_code=status_code,
        content={"code": code, "message": message, "data": res},
    )