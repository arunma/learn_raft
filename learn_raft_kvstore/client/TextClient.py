import json

import grpc
from google.protobuf.json_format import MessageToJson

from learn_raft.stubs.raft_pb2 import RequestVote
from learn_raft.stubs.raft_pb2_grpc import RaftStub
from learn_raft_kvstore.stubs.kvstore_pb2 import GetCommand
from learn_raft_kvstore.stubs.kvstore_pb2_grpc import KeyValueStoreStub


# Test client that sends a request to the KV/Raft service and prints the response
class TextClient:
    def __init__(self, port):
        host = "0.0.0.0"
        address = f"{host}:{port}"
        # We could reuse the channel considering it just represents a socket for same server
        channel = grpc.insecure_channel(address)
        self.kv_stub = KeyValueStoreStub(channel)
        self.raft_stub = RaftStub(channel)

    def request_vote(self, message):
        print(f"message {message}")
        print(f"Stub {self.raft_stub}")
        response = self.raft_stub.request_vote(request=RequestVote(server_id=1, term=1, last_log_term=1, last_log_index=1))
        value = MessageToJson(response)
        json_value = json.loads(value)
        print("json_value: " + str(json_value))
        return json_value

    def get(self, key):
        print(f"key {key}")
        response = self.kv_stub.get(request=GetCommand(key=key))
        value = MessageToJson(response)
        json_value = json.loads(value)
        print("json_value: " + str(json_value))
        return json_value
