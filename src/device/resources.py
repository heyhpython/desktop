"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: resources.py
@time: 2021/10/27 14:49
"""

from fastapi_admin.resources import Field
from fastapi_admin.widgets import displays, filters, inputs

from . import Device, Command
from src.utils.admin import Resource, ToManyDisplay, ForeignKeyDisplay


class DeviceResource(Resource):
    label = "设备"
    model = Device
    icon = "fas fa-admin"
    page_pre_title = "后台"
    page_title = "设备后台"
    filters = [
        filters.Search(name="name", label="设备名", search_mode="contains", placeholder="搜索设备名"),
        filters.Date(name="created_at", label="入网时间"),
        filters.Search(name="location", label="位置", search_mode="contains", placeholder="搜索位置"),
        filters.Search(name="pin", label="位置", search_mode="equal", placeholder="搜索PIN码"),

    ]
    fields = [
        "id",
        Field(name="name", label="名称"),
        Field(name="location", label="位置"),
        Field(name="pin", label="PIN脚"),
        Field('commands', label='命令', display=ToManyDisplay(), input_=inputs.DisplayOnly()),
        Field(name="created_at", label="入网时间", display=displays.DatetimeDisplay(), input_=inputs.DisplayOnly()),
    ]


class CommandResource(Resource):
    label = "命令"
    model = Command
    icon = "fas fa-admin"
    page_pre_title = "后台"
    page_title = "命令后台"
    filters = [
        filters.Search(name="command", label="命令", search_mode="contains", placeholder="搜索命令"),
        filters.Search(name="pattern", label="命中方式", search_mode="contains", placeholder="搜索命中方式"),
        filters.Date(name="created_at", label="入网时间"),

    ]
    fields = [
        "id",
        Field(name="command", label="命令"),
        Field(name="pattern", label="命中方式"),
        Field(name="created_at", label="入网时间", display=displays.DatetimeDisplay(), input_=inputs.DisplayOnly()),
        Field(name="device", label="所属设备", display=ForeignKeyDisplay(), input_=inputs.ForeignKey(Device)),
    ]

#
# app.register(DeviceResource)
# app.register(CommandResource)
