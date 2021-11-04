"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: displays.py
@time: 2021/11/3 14:44
"""
from typing import List
import json

from fastapi_admin.widgets import displays
from starlette.requests import Request
from tortoise import Model


class ToManyDisplay(displays.Display):
    template = "widgets/displays/json.html"

    async def render(self, request: Request, many: List[Model]):
        if many:
            many = [repr(sub) for sub in many]
        return await super(ToManyDisplay, self).render(request, json.dumps(many, ensure_ascii=False))


class ForeignKeyDisplay(displays.Display):
    async def render(self, request: Request, value):
        if value is None:
            value = ""
        if not self.template:
            return repr(value)
