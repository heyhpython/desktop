"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: __init__.py.py
@time: 2021/10/28 10:39
"""
from src.signals import after_boot
from .api import router


@after_boot.connect
def init_app(app):
    app.include_router(router, tags=['Jerry'])
