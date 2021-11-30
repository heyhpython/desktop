"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: models.py
@time: 2021/11/2 21:02
"""

from tortoise import fields
from src.utils.admin import ManyToOneModel, AbstractModel, AdminMixin, AdminMeta


class Command(AbstractModel, ManyToOneModel, AdminMixin):
    class Admin(AdminMeta):
        label = "命令"
        fields = {"command": "命令", "pattern": "出发方式", "device": "所属设备"}
        order = 2.1
        icon = "fas fa-terminal"

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


class Device(AbstractModel, AdminMixin):
    class Admin(AdminMeta):
        label = "设备"
        fields = {"name": "设备名", "location": "位置", "pin": "PIN脚", "commands": "命令"}
        icon = "fas fa-terminal"
        order = 2.0

    name = fields.CharField(max_length=32, description="设备名称")
    location = fields.CharField(max_length=32, description="设备位置")
    pin = fields.CharField(max_length=16, description="设备gpio pin脚号")

    def __str__(self):
        return f'{self.name} In:{self.location}'

    def __repr__(self):
        return str(self)


# @signals.post_save(Command)
# async def after_del(obj, **kwargs):
#     print("after save command ", obj, kwargs)
#     raise Exception()
