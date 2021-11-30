"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: __init__.py.py
@time: 2021/11/2 21:02
"""
from .models import Device, Command   # noqa
from . import resources   # noqa
from src.signals import after_boot


@after_boot.connect
def init_app(app):
    pass
