from learn_raft.stubs import raft_pb2_grpc


class RaftService(raft_pb2_grpc.RaftServicer):
    def __init__(self, raft_node):
        self.raft_node = raft_node

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

    def get_state(self, request, context):
        print("Calling get_state on RaftService")
        return self.raft_node.get_state(request)

    # Ideally, this function is internal and should not be exposed. It is only used for testing purposes.
    def start_election(self, request, context):
        print("Calling start_election on RaftService")
        return self.raft_node.start_election()
