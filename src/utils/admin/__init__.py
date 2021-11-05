"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: __init__.py.py
@time: 2021/11/3 19:27
"""
from .app import app
from .routers import router as api_router
from . import displays, resources, models
from .displays import Json, ToManyDisplay, ForeignKeyDisplay
from .resources import Resource
from .models import ManyToOneModel, AbstractModel, AdminMixin, AdminMeta

app.include_router(api_router)

__all__ = ['app'] + \
          displays.__all__ + \
          resources.__all__ + \
          models.__all__

