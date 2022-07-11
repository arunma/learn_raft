from learn_raft.stubs import raft_pb2_grpc


class RaftService(raft_pb2_grpc.RaftServicer):

    def __init__(self, raft_node):
        self.raft_node=raft_node

    def request_vote(self, request, context):
        return self.raft_node.state.request_vote(request)

    def append_entries(self, request, context):
        return self.raft_node.state.append_entries(request)


