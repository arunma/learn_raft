import grpc
from grpc import aio

from learn_raft.stubs import raft_pb2_grpc

class Peer:
    def __init__(self, server):
        self.server = server
        self.vote_granted = False

        self.next_index = None
        self.match_index = None

        # TODO last_log_term
        # TODO current_term

    async def start(self):
        # Start grpc client
        address = f"{self.server.host}:{self.server.port}"
        channel = grpc.insecure_channel(address)
        self.stub = raft_pb2_grpc.RaftStub(channel)
