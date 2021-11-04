"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: signals.py
@time: 2021/10/27 20:57
"""
from blinker import NamedSignal


configured = NamedSignal('CONFIGURED')  # 配置发送
after_boot = NamedSignal('AFTER_BOOT')  # 注册路由
