"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: base.py
@time: 2021/10/29 11:39
"""
import logging
import time
from abc import abstractmethod, ABC

import requests

logger = logging.getLogger(__name__)


class Session(requests.Session):

    def request(self, method: str, url, *args, **kwargs):
        s = time.time()
        resp = super(Session, self).request(method, url, *args, **kwargs)
        d = int((time.time() - s) * 1000)
        logger.info(f"{method} {url} args:{args} kwargs:{kwargs} status:{resp.status_code} "
                    f"response:{resp.json()} cost: {d} ms")
        return resp


class BaseClient:
    _CONFIG_NAMESPACE = 'BaseClient'
    config = {}

    @abstractmethod
    def get_name(self):
        """please implement in subclass"""

    @property
    def name(self):
        return self.get_name()

    @property
    def timeout(self):
        return self.config.get(f'{self.name}_TIMEOUT', 1)


class WebClient(BaseClient, ABC):
    _CONFIG_NAMESPACE = "WEB"

    def __init__(self, auth_header=None, token_prefix=None, env=None):
        self.session = Session()
        self.auth_header = auth_header if auth_header is not None else 'Authorization'
        self.token_prefix = token_prefix if token_prefix is not None else "Bearer "
        self.env = env
        self.endpoint = None
        self.token = None

    def init(self, config):
        config = config.get(self._CONFIG_NAMESPACE, {})[self.name]
        self.endpoint = config[self.endpoint_config_name].rstrip("/")
        self.token = config[self.token_config_name]
        self.session.headers[self.auth_header] = "{}{}".format(
            self.token_prefix, self.token
        )
        self.config = config

    def update_config(self, config):
        self.init(config)

    @property
    def endpoint_config_name(self):
        return "ENDPOINT"

    @property
    def token_config_name(self):
        return "TOKEN"

    def path_join(self, uri):
        return f"{self.endpoint}/{uri}"

    def get(self, path, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        full_path = self.path_join(path)
        resp = self.session.get(full_path, **kwargs)
        if resp.status_code == 404:
            logger.warning("GET from %s not found. path: %s kwargs: %s" % (
                self.name, path, kwargs))
            return dict()
        resp.raise_for_status()
        return resp.json()

    def post(self, path, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        full_path = self.path_join(path)
        resp = self.session.post(full_path, **kwargs)
        if resp.status_code == 404:
            logger.warning("GET from %s not found. path: %s kwargs: %s" % (
                self.name, path, kwargs))
            return dict()
        resp.raise_for_status()
        return resp.json()
