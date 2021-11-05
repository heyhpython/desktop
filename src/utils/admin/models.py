"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: models.py
@time: 2021/11/3 22:33
"""
import abc
import dataclasses
from typing import Optional, List, Union, Callable, Any, Tuple, Dict, Type
import datetime

import tortoise
from fastapi_admin import resources
from fastapi_admin.widgets import inputs, displays, filters
from pydantic import BaseModel

from .displays import ToManyDisplay, ForeignKeyDisplay
from .resources import Resource
from .app import app


class ManyToOneModel:
    @abc.abstractmethod
    def render(self):
        raise NotImplemented


def get_display(f: tortoise.fields.Field):
    if isinstance(f, tortoise.ManyToManyFieldInstance):
        # 多对多
        return ToManyDisplay()
    if isinstance(f, tortoise.ForeignKeyFieldInstance):
        # 多对一
        return ForeignKeyDisplay()
    if isinstance(f, tortoise.BackwardFKRelation):
        # 一对多
        return ToManyDisplay()
    if f.field_type is datetime.date:
        return displays.DateDisplay()
    elif f.field_type is datetime.datetime:
        return displays.DatetimeDisplay()
    elif f.field_type in (dict, list):
        return displays.Json()
    else:
        return


def get_input(f: tortoise.fields.Field):
    if isinstance(f, tortoise.ManyToManyFieldInstance):
        # 多对多
        return inputs.ManyToMany(f.related_model)
    if isinstance(f, tortoise.ForeignKeyFieldInstance):
        # 多对一
        return inputs.ForeignKey(f.related_model)
    if isinstance(f, tortoise.BackwardFKRelation):
        # 一对多
        return inputs.DisplayOnly()
    if f.field_type is datetime.date:
        return inputs.Date()
    elif f.field_type is datetime.datetime:
        return inputs.DateTime()
    elif f.field_type in (dict, list):
        return inputs.Json()
    else:
        return


class ResourceData(BaseModel):
    label: str
    icon: str = ''
    model: Type[tortoise.Model]
    fields: List = []  # [Union[str, resources.Field, resources.ComputeField]]
    page_size: int = 10
    page_pre_title: Optional[str] = None
    page_title: Optional[str] = None
    filters: List = []
    order: float = 1.0


class AdminMeta:
    icon: str = "fas fa default"
    label: str
    fields: Optional[Dict[str, str]]
    filters = []
    page_size: int = 10
    page_pre_title: Optional[str] = None
    page_title: Optional[str] = None
    order: float = 1.0


class AdminMixin:

    class Admin(AdminMeta):
        pass

    @classmethod
    def admin_get_resource(cls) -> Type[Resource]:
        data = ResourceData(model=cls, label=cls.Admin.label, icon=cls.Admin.icon, order=cls.Admin.order)
        data.fields = cls.admin_get_fields()
        data.filters = cls.admin_get_filters()
        resource_cls = type(f'{cls.__name__}Resource', (Resource,), data.dict())
        return resource_cls

    @classmethod
    def admin_register(cls):
        app.register(cls.admin_get_resource())

    @classmethod
    def admin_get_fields(cls):
        fields = []
        for name, label in cls.Admin.fields.items():
            label = label or name
            field: resources.Field = getattr(cls.Admin, name, None)
            if field:
                field.label = label
                fields.append(field)
                continue
            else:
                if name not in cls._meta.fields_map:
                    display = input_ = None
                else:
                    db_field = cls._meta.fields_map[name]
                    input_ = get_input(db_field)
                    display = get_display(db_field)
                fields.append(resources.Field(name, label=label, display=display, input_=input_))
        return fields

    @classmethod
    def admin_get_filters(cls):
        return cls.Admin.filters


class AbstractModel(tortoise.Model):
    class Meta:
        abstract = True

    id = tortoise.fields.IntField(pk=True, description="主键")
    created_at = tortoise.fields.DatetimeField(auto_now_add=True, index=True, description='创建时间')
    updated_at = tortoise.fields.DatetimeField(auto_now=True, index=True, description='更新时间')


__all__ = ['AbstractModel', 'AdminMixin', 'ManyToOneModel', "AdminMeta"]
