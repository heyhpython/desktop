"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: models.py
@time: 2021/11/3 22:33
"""
import abc

from tortoise import Model


class ManyToOneModel:
    @abc.abstractmethod
    def render(self):
        raise NotImplemented

    # @classmethod
    # @abc.abstractmethod
    # def parse(cls, data):
    #     raise NotImplemented
