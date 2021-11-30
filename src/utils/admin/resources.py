"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: resources.py
@time: 2021/11/3 14:46
"""
from typing import Optional
import logging

from tortoise import Model
from fastapi_admin.resources import Field, Model as BaseResource, ComputeField
from fastapi_admin.widgets import displays, inputs
from starlette.requests import Request
from starlette.datastructures import FormData

logger = logging.getLogger(__name__)


class Resource(BaseResource):
    order: float = 1.0

    @classmethod
    async def get_inputs(cls, request: Request, obj: Optional[Model] = None):
        ret = []
        for field in cls.get_fields(is_display=False):
            input_ = field.input
            if isinstance(input_, inputs.DisplayOnly):
                continue
            if isinstance(input_, inputs.File):
                cls.enctype = "multipart/form-data"
            name = input_.context.get("name")
            if name in cls.model._meta.m2m_fields and obj:
                await obj.fetch_related(name)

            ret.append(await input_.render(request, getattr(obj, name, None)))
        return ret

    @classmethod
    def get_fields(cls, is_display: bool = True):
        ret = []
        _meta = cls.model._meta
        pk_column = _meta.db_pk_column
        for field in cls.fields or _meta.fields:
            if isinstance(field, str):
                if field == pk_column:
                    continue
                field = cls._get_display_input_field(field)
            if isinstance(field, ComputeField) and not is_display:
                continue
            elif isinstance(field, Field):
                if field.name == pk_column:
                    continue
                if (is_display and isinstance(field.display, displays.InputOnly)) or (
                        not is_display and isinstance(field.input, inputs.DisplayOnly)
                ):
                    continue
            if (
                    field.name in _meta.fetch_fields
                    and field.name not in _meta.fk_fields | _meta.m2m_fields | _meta.backward_fk_fields
            ):
                continue
            ret.append(field)
        ret.insert(0, cls._get_display_input_field(pk_column))
        return ret

    @classmethod
    def get_2m_fields(cls):
        ret = []
        for field in cls.fields or cls.model._meta.fields:
            if isinstance(field, Field):
                field = field.name
            if field in cls.model._meta.m2m_fields | cls.model._meta.backward_fk_fields | cls.model._meta.fk_fields:
                ret.append(field)
        return ret

    @classmethod
    async def resolve_data(cls, request: Request, data: FormData):
        ret = {}
        m2m_ret = {}
        for field in cls.get_fields(is_display=False):
            input_ = field.input
            if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                continue
            name = input_.context.get("name")
            if isinstance(input_, inputs.ManyToMany):
                v = data.getlist(name)
                value = await input_.parse_value(request, v)
                m2m_ret[name] = await input_.model.filter(pk__in=value)
            else:
                v = data.get(name)
                value = await input_.parse_value(request, v)
                if value is None:
                    continue
                ret[name] = value
        return ret, m2m_ret


__all__ = ['Resource']
