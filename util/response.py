from fastapi.responses import JSONResponse

def returnJson(data=None, message="Success", code=200, status_code=200):
    '''
    返回Json数据
    '''
    return JSONResponse(
        status_code=status_code,
        content={"code": code, "message": message, "data": data},
    )