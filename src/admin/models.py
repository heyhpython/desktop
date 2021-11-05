"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: models.py
@time: 2021/10/27 14:30
"""
from tortoise import fields
from fastapi_admin.models import AbstractAdmin
from fastapi_admin import resources
from fastapi_admin.widgets import displays, inputs
from src.utils.admin.models import AdminMixin, AdminMeta, AbstractModel, app


class User(AbstractAdmin, AbstractModel, AdminMixin):
    """
    用户
    """

    class Admin(AdminMeta):
        label = "用户"
        icon = "fas fa-user"
        fields = {"id": "", "username": "用户名", "roles": "权限列表", "password": None, "avatar": None, "email": "邮箱",
                  "created_at": "创建时间",
                  }
        password = resources.Field('password', label="密码", display=displays.InputOnly(), input_=inputs.Password())
        avatar = resources.Field('avatar', label="头像", display=displays.Image(width='40'),
                                 input_=inputs.Image(app.upload))
        order = 1.0

    id = fields.IntField(pk=True, description="主键")
    created_at = fields.DatetimeField(auto_now_add=True, index=True, description='创建时间')
    updated_at = fields.DatetimeField(auto_now=True, index=True, description='更新时间')
    mobile = fields.CharField(max_length=11, index=True, description='手机号', null=True)
    avatar = fields.TextField(description='头像地址', null=True)
    email = fields.CharField(max_length=128, index=True, description="邮箱", null=True)

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username


class Role(AbstractModel, AdminMixin):
    """
    角色
    """

    class Admin(AdminMeta):
        label = "角色"
        icon = "fak fa-critical-role"
        fields = {"id": "", "name": "角色名", "users": "用户列表"}
        order = 1.1

    name = fields.CharField(max_length=32, index=True, unique=True, description="角色名")
    users = fields.ManyToManyField('models.User', related_name='roles', through='users_roles')
    id = fields.IntField(pk=True, description="主键")
    created_at = fields.DatetimeField(auto_now_add=True, index=True, description='创建时间')
    updated_at = fields.DatetimeField(auto_now=True, index=True, description='更新时间')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
