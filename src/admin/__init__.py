"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: __init__.py.py
@time: 2021/10/27 14:30
"""
from . import resources  # noqa
from . import api
from .models import User, Role
from src.signals import after_boot


@after_boot.connect
def init_app(app):
    app.include_router(api.router, tags=['Jerry'])
