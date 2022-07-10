import asyncio
import random
import threading
from enum import Enum

from learn_raft.raft import server_tostring, peer_tostring
from learn_raft.raft.peer import Peer
from learn_raft.stubs.raft_pb2 import RequestVote, RequestVoteResponse


class NodeState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3


class RaftNode:
    def __init__(self, local_server, all_servers, config, node_state=NodeState.FOLLOWER):
        self.server=local_server
        self.node_state=node_state
        self.config=config

        #Persistent state
        self.log=[]
        self.voted_for=None
        self.current_term=0

        #Volatile state on all servers
        self.commit_index=None
        self.last_applied_index=None

        #Volatile state on leaders - stored inside peer object
        self.all_servers=all_servers
        self.peer_map={}

        self.state_machine = None

    async def start(self):
        for server in self.all_servers:
            if server.id!=self.server.id and server_tostring(server) not in self.peer_map:
                peer = Peer(server)
                await peer.start()
                self.peer_map[server_tostring(server)]=peer

        #start election
        self.start_election_timer()


    def start_election_timer(self):
        interval_from = self.config['election_timeout_from']
        interval_to = self.config['election_timeout_to']
        interval = interval_from + (interval_to - interval_from) * random.random()
        print(f"Starting election timer for {self.server.id} at interval {interval} seconds")
        thread=threading.Timer(interval, self.start_election)
        #thread.daemon=True
        thread.start()
        print(f"Election thread started for {self.server.id}")

    def start_election(self):
        print(f"Called start_election in RAFT_NODE: {self.server.id}")
        peer_votes=[]
        for id, peer in self.peer_map.items():
            if peer.server.id == self.server.id:
                continue
            next_term = self.current_term + 1
            request = RequestVote(server_id=self.server.id, term=next_term, last_log_term=self.current_term, last_log_index=len(self.log))
            p1 = self.get_vote_from_server(peer, request)
            peer_votes.append(p1)
        vote_responses = peer_votes
        print(f"Vote responses for {self.server.id} are: {vote_responses}")
        return vote_responses


    def get_vote_from_server(self, peer, request):
        vote_response = peer.stub.request_vote(request)
        return vote_response


    def leader_id(self):
        #FIXME return the proper leader id
        return "xxxx"


    def append_entries(self, request):
        print("Called append_entries in RAFT_NODE")
        pass

    def request_vote(self, request):
        #print("******************* Called request_vote in RAFT_NODE. Giving the vote blindly")
        if self.current_term < request.term:
            self.current_term = request.term
            self.voted_for = request.server_id
            return RequestVoteResponse(server_id=self.server.id, term=request.term, vote_granted=True)
        else:
            return RequestVoteResponse(server_id=self.server.id, term=request.term, vote_granted=False)

