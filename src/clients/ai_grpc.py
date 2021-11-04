"""
@author: yuhao.he
@contact: <hawl.yuhao.he@gmail.com>
@version: 0.0.1
@file: ai_grpc.py
@time: 2021/10/28 20:37
"""
import grpc

from src.proto import service_pb2, service_pb2_grpc
from src.utils import BaseClient


class AiClient(BaseClient):
    _CONFIG_NAMESPACE = "GRPC_CLIENT"

    def get_name(self):
        return "AI"

    def __init__(self):
        self.stub:  service_pb2_grpc.AiStub = None

    def ask(self, q) -> str:
        resp: service_pb2.AskReply = self.stub.ask(service_pb2.AskRequest(question=q))
        return resp.reply

    def add_command(self, pattern, template) -> bool:
        resp: service_pb2.SuccessResponse = self.stub.add_command(
            service_pb2.AddCommandRequest(pattern=pattern, template=template))
        return resp.success

    def init(self, config):
        self.config = config.get(self._CONFIG_NAMESPACE, {}).get(self.get_name())
        self.stub = service_pb2_grpc.AiStub(grpc.insecure_channel(self.config['ENDPOINT']))


if __name__ == "__main__":
    client = AiClient()
    client.ask("1")
