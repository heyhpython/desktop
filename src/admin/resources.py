"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: resources.py
@time: 2021/10/27 14:49
"""
import logging

from fastapi_admin.file_upload import FileUpload
from fastapi_admin.resources import Field
from fastapi_admin.widgets import displays, filters, inputs

from .models import User, Role
from src.constants import __upload__
from src.utils.admin import Resource, ToManyDisplay, app

logger = logging.getLogger(__name__)
upload = FileUpload(uploads_dir=__upload__)


class UserResource(Resource):
    label = "用户"
    model = User
    icon = "fas fa-admin"
    page_pre_title = "后台"
    page_title = "用户后台"
    filters = [
        filters.Search(
            name="username", label="用户名", search_mode="contains", placeholder="搜索用户名"
        ),
        filters.Date(name="created_at", label="入网时间"),
    ]
    fields = [
        "id",
        Field(name="username", label="用户名"),
        Field(
            name="password",
            label="密码",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="email", label="邮箱", input_=inputs.Email()),
        Field(
            name="avatar",
            label="头像",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
        Field(name="created_at", label="入网时间", display=displays.DatetimeDisplay(), input_=inputs.DisplayOnly()),
        Field('roles', label='角色', display=ToManyDisplay(), input_=inputs.ManyToMany(Role)),
    ]


class RoleResource(Resource):
    label = "角色"
    model = Role
    icon = "fas fa-admin"
    page_pre_title = "后台"
    page_title = "角色管理"
    filters = [
        filters.Search(
            name="name", label="角色名", search_mode="contains", placeholder="搜索角色名"
        ),
        filters.Date(name="created_at", label="入网时间"),
    ]
    fields = [
        "id",
        Field(name="name", label="角色名"),
        Field('users', label='角色', display=ToManyDisplay(), input_=inputs.ManyToMany(User)),
        Field(name="created_at", label="入网时间", display=displays.DatetimeDisplay(), input_=inputs.DisplayOnly()),
    ]


# app.register(UserResource)
# app.register(RoleResource)
