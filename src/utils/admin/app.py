"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: app.py
@time: 2021/11/5 11:34
"""
from fastapi_admin.app import FastAPIAdmin, middlewares, BaseHTTPMiddleware
from fastapi_admin.file_upload import FileUpload

from src.constants import __upload__


app = FastAPIAdmin(
    title="FastAdmin",
    description="A fast admin dashboard based on fastapi and tortoise-orm with tabler ui.",
)
app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.language_processor)
app.upload = FileUpload(uploads_dir=__upload__)
