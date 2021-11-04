"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: validators.py
@time: 2021/10/28 10:00
"""
from typing import Optional

from pydantic import BaseModel


class Answer(BaseModel):
    instruction: Optional[str]
    message: str


class Question(BaseModel):
    message: str
