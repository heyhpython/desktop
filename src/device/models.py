"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: models.py
@time: 2021/11/2 21:02
"""

from tortoise import Model, fields
from src.utils.admin.models import ManyToOneModel


class AbstractModel(Model):
    class Meta:
        abstract = True
        # fetch_fields = ('commands', )
        # fk_fields = ()

    id = fields.IntField(pk=True, description="主键")
    created_at = fields.DatetimeField(auto_now_add=True, index=True, description='创建时间')
    updated_at = fields.DatetimeField(auto_now=True, index=True, description='更新时间')


class Command(AbstractModel, ManyToOneModel):
    command = fields.CharField(max_length=32, description="命令 注册到ai中心 即AI answer 接口的输出")
    pattern = fields.CharField(max_length=128, description="用于唤醒命令，即AI answer 接口的输入")
    device = fields.ForeignKeyField("models.Device", related_name="commands", db_constraint=False)

    def __repr__(self):
        return f"<{self.pattern}: {self.command}>"

    def __str__(self):
        return f"<{self.pattern}: {self.command}>"

    async def render(self):
        return {"command": self.command, "pattern": self.pattern, "id": self.id}

    @classmethod
    async def parse(cls, data: dict):
        if 'id' in data:
            pk = data.pop('id')
            obj = await cls.get(id=pk)
            for k, v in data:
                setattr(obj, k, v)
        else:
            obj = await cls(**data)
        return obj


class Device(AbstractModel):
    name = fields.CharField(max_length=32, description="设备名称")
    location = fields.CharField(max_length=32, description="设备位置")
    pin = fields.CharField(max_length=16, description="设备gpio pin脚号")

    def __str__(self):
        return f'{self.name} In:{self.location}'

    def __repr__(self):
        return str(self)