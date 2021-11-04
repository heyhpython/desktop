"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: resources.py
@time: 2021/10/27 14:49
"""

from fastapi import APIRouter, Depends
from fastapi_admin.utils import check_password

from src.errors import AuthErr
from src.utils import login, login_required
from .models import User
from .validators import Login, LoginReturn, UserInfo


router = APIRouter(prefix='/jerry')


@router.post('/login', response_model=LoginReturn)
async def client_login(body: Login):
    """
    客户端登录
    """
    user = await User.filter(username=body.username).prefetch_related('roles').get_or_none()
    if not user or not check_password(body.password, user.password):
        raise AuthErr(message=f"Login fail for username {body.username}")
    token = login(user)
    return {
        "token": token
    }


@router.get('/who-am-i', response_model=UserInfo, response_model_exclude_unset=True)
async def who_am_i(user_payload=Depends(login_required)):
    """
    获取用户身份
    """
    user, payload = user_payload
    return payload['user']
