import json
import grpc
from google.protobuf.json_format import MessageToJson

from learn_raft.stubs.raft_pb2 import HelloRequest
from learn_raft.stubs.raft_pb2_grpc import GreeterStub


class TextClient:
    def __init__(self):
        self._stub = None

    def start(self, port):
        if not self._stub:
            host = "localhost"
            address = f"{host}:{port}"
            channel = grpc.insecure_channel(address)
            self.stub = GreeterStub(channel)

    def say_hello(self, message):
        print(f"message {message}")
        response, call = self.stub.say_hello.with_call(request=HelloRequest(name=message))
        value = MessageToJson(response)
        metadata = [dict(name=key, value=value) for key, value in call.trailing_metadata()]
        print('metadata: ' + str(metadata))

        json_value = json.loads(value)
        return json_value
