"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: __init__.py.py
@time: 2021/10/29 11:33
"""
from src.signals import configured
from .ai_grpc import AiClient


ai_client = AiClient()


@configured.connect
def init_config(config):
    ai_client.init(config)
