"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 1.0.0
@file: jwt_utils.py
@time: 2021/10/22 18:39
"""
import time
import typing as t
import jwt
from starlette.requests import Request

from src.errors import AuthErr
from src.utils.constants import SECRET, AUTH_HEADERS


async def login_required(request: Request):
    from src.admin.models import User
    token = request.headers.get(AUTH_HEADERS)
    try:
        payload: dict = jwt.decode(token, SECRET, verufy=True, algorithms=['HS256'])
    except Exception:
        raise AuthErr("Auth Fail Bad token")
    return await User.filter(username=payload['user']['username']).prefetch_related('roles').get_or_none(), payload


def login(user) -> t.Union[str, bytes]:
    payload = {
        "user": {
            'username': user.username,
            'email': user.email,
            'avatar': user.avatar,
            "roles": [role.name for role in user.roles]
        },
        'iat': time.time(),
        'exp': time.time() + 24 * 3600 * 30,
        'iss': "Jerry.alot",
    }
    return jwt.encode(payload, SECRET)
