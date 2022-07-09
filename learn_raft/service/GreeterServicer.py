from learn_raft.stubs import raft_pb2_grpc
from learn_raft.stubs import raft_pb2


class GreeterServicer(raft_pb2_grpc.GreeterServicer):
    def say_hello(self, request, context):
        print("Saying Hello")
        name = request.name
        print(f"Name is {name}")
        return raft_pb2.HelloReply(message=f"HELLO {name}")
