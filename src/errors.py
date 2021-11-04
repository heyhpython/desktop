"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: errors.py
@time: 2021/10/27 20:00
"""


class BaseResponseError(Exception):
    code = None
    message = ""

    def __init__(self, code=None, message=None):
        if code is not None:
            self.code = code
        if message is not None:
            self.message = message


class NotFoundError(BaseResponseError):
    code = 404


class WeChatError(BaseResponseError):
    code = 500


class ValidateError(BaseResponseError):
    code = 400


class AuthErr(BaseResponseError):
    code = 401
    message = "NOT AUTH"
