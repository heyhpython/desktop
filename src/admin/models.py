"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: models.py
@time: 2021/10/27 14:30
"""
from tortoise import fields, models
from fastapi_admin.models import AbstractAdmin


class User(AbstractAdmin):
    """
    用户
    """
    search_fields = ('username',)

    class Meta:
        fetch_fields = {'roles', }

    id = fields.IntField(pk=True, description="主键")
    created_at = fields.DatetimeField(auto_now_add=True, index=True, description='创建时间')
    updated_at = fields.DatetimeField(auto_now=True, index=True, description='更新时间')
    mobile = fields.CharField(max_length=11, index=True, description='手机号', null=True)
    avatar = fields.TextField(description='头像地址', null=True)
    email = fields.CharField(max_length=128, index=True, description="邮箱", null=True)


class Role(models.Model):
    name = fields.CharField(max_length=32, index=True, unique=True, description="角色名")
    users = fields.ManyToManyField('models.User', related_name='roles', through='users_roles')
    id = fields.IntField(pk=True, description="主键")
    created_at = fields.DatetimeField(auto_now_add=True, index=True, description='创建时间')
    updated_at = fields.DatetimeField(auto_now=True, index=True, description='更新时间')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
