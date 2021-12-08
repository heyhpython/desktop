"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: mqtt_client.py
@time: 2021/12/7 14:09
"""
import logging
import uuid
import typing as t

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class InfoMqttMixin(mqtt.Client):
    app: None
    topics: t.List[t.Tuple] = []
    config = {}

    def __init__(self, config=None):
        self.config = config['MQTT'] if config else {}
        super().__init__(client_id=uuid.uuid4().hex)

    def init(self, config):
        self.config = config['MQTT']
        self.host = self.config['BROKER_HOST']
        self.port = self.config.get('BROKER_PORT', 1883)

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, val: str):
        self._host = val

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, val: str):
        self._port = val

    def run(self):
        self.connect(self.host, port=self.port)
        self.subscribe(self.topics)
        self.loop_forever()

    def register(self, topic: t.Union[str, t.Tuple, t.List]):
        if isinstance(topic, str):
            self.topics.append((topic, 0))
        else:
            self.topics.append((topic[0], topic[1]))


mqtt_client = InfoMqttMixin()


def on_connect(self: InfoMqttMixin, userdata, flags, rc, *args, **kwargs):
    logger.info("Connect to %s: %s %s ", self.host, self.port, rc)


def on_subscribe(self: InfoMqttMixin, userdata, mid, rc, *args, **kwargs):
    logger.info("Subscribe %s ", rc)


def on_message(self: InfoMqttMixin, userdata, message: mqtt.MQTTMessage):
    logger.info("Get message %s from %s at ", message.payload, message.topic, message.timestamp)
    # todo save in db


def on_publish(self: InfoMqttMixin, userdata, mid):
    pass


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_subscribe = on_subscribe
mqtt_client.on_publish = on_publish

