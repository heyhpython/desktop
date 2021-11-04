"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: api.py
@time: 2021/10/28 10:43
"""
from fastapi import APIRouter, Depends

from .validators import Answer, Question
from src.utils.jwt_utils import login_required

router = APIRouter(prefix='/jerry')


@router.post('/ask', response_model=Answer, dependencies=[Depends(login_required)])
async def ask(question: Question):
    """
    用户提问 执行指令并响应
    """
    return Answer(message="OK")
