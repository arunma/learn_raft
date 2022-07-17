import grpc

from learn_raft.stubs import raft_pb2_grpc


class Peer:
    def __init__(self, server):
        self.server = server
        self.stub = raft_pb2_grpc.RaftStub(grpc.insecure_channel(self.server.host + ":" + str(self.server.port)))

        # TODO last_log_term
        # TODO current_term

    # async def start(self):
    #     # Start grpc client
    #     address = f"{self.server.host}:{self.server.port}"
    #     channel = grpc.insecure_channel(address)
    #     self.stub = raft_pb2_grpc.RaftStub(channel)
