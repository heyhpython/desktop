"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: validators.py
@time: 2021/10/28 10:00
"""
from typing import List, Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from .models import User


class Login(BaseModel):
    username: str
    password: str


class LoginReturn(BaseModel):
    token: str


class RoleInfo(BaseModel):
    name: str


UserBase = pydantic_model_creator(User, name='UserBase', include=('username', 'avatar', 'email'))


class UserInfo(UserBase):
    roles: Optional[List[str]]
