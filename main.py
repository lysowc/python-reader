from fastapi import FastAPI, Request
import importlib
import pkgutil
import api

app = FastAPI(title="identify api")


def normalize_path(*parts):
    """
    拼接 URL 路径，自动处理多余的斜杠
    """
    path = "/".join(
        str(p).strip("/")  # 去掉每部分头尾的 /
        for p in parts
        if p is not None and str(p).strip("/") != ""
    )
    leading = "/" if parts and str(parts[0]).startswith("/") else ""
    trailing = "/" if parts and str(parts[-1]).endswith("/") else ""
    return f"{leading}{path}{trailing}".replace("//", "/")


# 自动注册 router 模块下的所有路由
def register_router():
    for _, name, _ in pkgutil.iter_modules(api.__path__, api.__name__ + "."):
        module = importlib.import_module(name)
        if hasattr(module, "router"):
            prefix = getattr(
                module, "router_prefix", ""
            )  # 例如: "user" 或 "/user" 或 ""
            # 使用 normalize_path 安全拼接
            full_prefix = normalize_path("/api", prefix)
            app.include_router(module.router, prefix=full_prefix)


register_router()

from fastapi.exceptions import RequestValidationError
from util.response import returnJson


# 自定义异常处理器
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 自定义错误响应格式
    return returnJson(status_code=422, message=exc.errors())
