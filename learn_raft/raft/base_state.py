from learn_raft.raft import server_tostring
from learn_raft.raft.peer import Peer
from learn_raft.stubs.raft_pb2 import RequestVoteResponse


class BaseState:
    def __init__(self, state):
        self.state = state

    async def init_peers(self):
        for server in self.state.all_servers:
            if server.id != self.state.server_info.id and server_tostring(server) not in self.state.peer_map:
                peer = Peer(server)
                await peer.start()
                self.state.peer_map[server_tostring(server)] = peer

    # This function is called when the peers request for vote from this node
    def request_vote(self, request):
        print(
            "******************* Called request_vote in RAFT_NODE. Giving the vote slightly intelligently *******************")
        if self.state.current_term < request.term and not self.state.voted_for:
            self.state.current_term = request.term
            self.state.voted_for = request.server_id
            return RequestVoteResponse(server_id=self.state.server_info.id, term=request.term, vote_granted=True)
        else:
            return RequestVoteResponse(server_id=self.state.server_info.id, term=request.term, vote_granted=False)
