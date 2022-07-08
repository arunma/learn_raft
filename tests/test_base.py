import json

import grpc
from google.protobuf.json_format import MessageToJson
from learn_raft.raft_pb2 import HelloRequest
from learn_raft.raft_pb2_grpc import GreeterStub


def test_base():
    channel = grpc.insecure_channel("localhost")
    stub = GreeterStub(channel)

    print ("method: ", stub.SayHello._method.decode())

    response, call = stub.SayHello.with_call(
        request=HelloRequest(name=" ARUN ")
    )

    value = MessageToJson(response)
    val_json =(json.loads((value)))

    print (val_json)