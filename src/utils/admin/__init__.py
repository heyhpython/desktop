"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: __init__.py.py
@time: 2021/11/3 19:27
"""
from . import displays, resources, models
from .app import app
from .displays import Json, ToManyDisplay, ForeignKeyDisplay  # noqa
from .models import ManyToOneModel, AbstractModel, AdminMixin, AdminMeta  # noqa
from .resources import Resource  # noqa
from .routers import router as api_router

app.include_router(api_router)

__all__ = ['app'] + displays.__all__ + resources.__all__ + models.__all__
