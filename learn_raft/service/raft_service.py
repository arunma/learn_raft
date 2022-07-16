from learn_raft.stubs import raft_pb2_grpc


class RaftService(raft_pb2_grpc.RaftServicer):

    def __init__(self, raft_node):
        self.raft_node=raft_node

    def request_vote(self, request, context):
        return self.raft_node.request_vote(request)

    def append_entries(self, request, context):
        return self.raft_node.append_entries(request)

    def add_node(self, request, context):
        print("Calling add_node on RaftService")
        return self.raft_node.add_node(request)

    def remove_node(self, request, context):
        print("Calling remove_node on RaftService")
        return self.raft_node.remove_node(request)

