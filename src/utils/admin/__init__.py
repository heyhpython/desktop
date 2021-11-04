"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: __init__.py.py
@time: 2021/11/3 19:27
"""
from fastapi_admin.app import FastAPIAdmin, middlewares, BaseHTTPMiddleware
from .routers import router as api_router
from .displays import ToManyDisplay, ForeignKeyDisplay
from .inputs import ManyToManyInput
from .resources import Resource, ToManyField


app = FastAPIAdmin(
    title="FastAdmin",
    description="A fast admin dashboard based on fastapi and tortoise-orm with tabler ui.",
)
app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.language_processor)

app.include_router(api_router)

__all__ = ['app', 'FastAPIAdmin', 'ToManyDisplay', 'ForeignKeyDisplay', 'ManyToManyInput', 'Resource', 'ToManyField']
