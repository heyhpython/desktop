"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: __init__.py.py
@time: 2021/10/29 11:33
"""
from src.signals import configured
from .ai_grpc import AiClient
from .mqtt_client import mqtt_client


ai_client = AiClient()


@configured.connect
def init_config(config):
    ai_client.init(config)
    mqtt_client.init(config)


__all__ = [
    'AiClient', 'ai_client', 'mqtt_client'
]
