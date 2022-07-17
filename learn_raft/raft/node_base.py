import grpc

from learn_raft.raft import server_tostring, state_tostring
from learn_raft.raft.peer import Peer
from learn_raft.raft.transitioner import Transitioner
from learn_raft.stubs import cluster_manager_pb2_grpc
from learn_raft.stubs.raft_pb2 import RequestVoteResponse, RemoveNodeResponse, AddNodeResponse, RESULT_SUCCESS


class NodeBase:
    def __init__(self, state):
        print(f"State initialized as {state_tostring(state)}")
        self.state = state
        self.transitioner=Transitioner()
        self.cluster_manager_channel = grpc.insecure_channel(self.state.cluster_manager_ip)
        self.cluster_manager = cluster_manager_pb2_grpc.ClusterManagerStub(self.cluster_manager_channel)

    # async def init_peers(self):
    #     for server in self.state.all_servers:
    #         if server.id != self.state.server.id and server_tostring(server) not in self.state.peer_map:
    #             peer = Peer(server)
    #             await peer.start()
    #             self.state.peer_map[server_tostring(server)] = peer

    def add_node(self, request):
        print(f"******************* Calling add_node of {request.server.id} on {self.state.server.id} *******************")
        if request.server.id == self.state.server.id:
            print("******************* Attempting to add current node as peer. Ignoring *******************")
            return AddNodeResponse(result=RESULT_SUCCESS)

        print(f"******************* Adding node id {request.server.id} as PEER to Node : {server_tostring(self.state.server)} *******************")
        if request.server.id in self.state.peer_map:
            #Remove and add peer again
            print(f"Node {request.server.id} already found in peer map of {server_tostring(self.state.server)}. Removing and adding again.")
            del self.state.peer_map[request.server.id]
            self.state.peer_map[request.server.id] = Peer(request.server)
            self.print_peer_map()
            return AddNodeResponse(result=RESULT_SUCCESS)
        else:
            print(f"YESSSSSS !!! Adding node {request.server.id} to the peer map of {server_tostring(self.state.server)}.")
            self.state.peer_map[request.server.id] = Peer(request.server)
            self.print_peer_map()
            return AddNodeResponse(result=RESULT_SUCCESS)

    def remove_node(self, request):
        print(f"De-registering Raft Server node {request.id}")
        if request.id in self.state.peer_map:
            print(f"Removing node {request.id} from the peer map of {server_tostring(self.state.server)}")
            del self.state.peer_map[request.id]
            # Open up for election if the leader goes down
            if self.state.voted_for == request.id:
                self.state.voted_for = None
            self.print_peer_map()
            return RemoveNodeResponse(result=True)
        else:
            print(f"Node id {request.id} not found in peer map of {server_tostring(self.state.server)}. Nothing to do.")
            self.print_peer_map()
            return RemoveNodeResponse(result=True)

    # This function is called when the peers request for vote from this node
    def request_vote(self, request):
        # print("******************* Called request_vote in RAFT_NODE. Giving the vote slightly intelligently *******************")
        if self.state.current_term < request.term and not self.state.voted_for:
            self.state.current_term = request.term
            self.state.voted_for = request.server_id
            return RequestVoteResponse(server_id=self.state.server.id, term=request.term, voted_for=self.state.voted_for)
        else:
            return RequestVoteResponse(server_id=self.state.server.id, term=request.term, voted_for=self.state.voted_for)


    def has_majority_votes(self, yays):
        replication_factor = self.state.config['replication_factor']
        return yays > (replication_factor - 1) / 2

    def print_peer_map(self):
        print(f"******************* Peer Map of {server_tostring(self.state.server)} *******************")
        for peer in self.state.peer_map.values():
            print(f"{peer.server.id}")
        print("******************* End of Peer Map *******************")