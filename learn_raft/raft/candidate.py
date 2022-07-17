import threading
from random import random

from learn_raft.raft import state_tostring, server_tostring
from learn_raft.raft.node_base import NodeBase
from learn_raft.raft.follower import Follower
from learn_raft.raft.timer import Timer
from learn_raft.stubs.raft_pb2 import RequestVote


class Candidate(NodeBase):
    def __init__(self, state):
        super().__init__(state)
        self.start_election_timer()

    def start_election_timer(self):
        interval = self.state.election_timeout_from + (self.state.election_timeout_to - self.state.election_timeout_from) * random()
        print(f"Starting election timer for {self.state.server.id} at interval {interval} seconds")
        self.election_timer = Timer(interval, self.start_election, self.state.server.id, "candidate")
        self.election_timer.start()
        #self.start_election()
        print(f"Election thread started for {self.state.server.id}")

    def start_election(self):
        print(f"Called start_election (state) in RAFT_NODE: {state_tostring(self.state)}")
        print(f"Called start_election (server_info) in RAFT_NODE: {server_tostring(self.state.server)}")
        print(f"Called start_election in RAFT_NODE: {self.state.server.id}")
        peer_votes = []
        print(f"Peer map items : {self.state.peer_map.items()}")
        yay_votes = 0
        # Vote for self
        if not self.state.voted_for:
            yay_votes += 1
            self.voted_for = self.state.server.id

        # Gather votes
        for id, peer in self.state.peer_map.items():
            if peer.server.id == self.state.server.id:
                continue
            next_term = self.state.current_term + 1
            request = RequestVote(server_id=self.state.server.id,
                                  term=next_term,
                                  last_log_term=self.state.current_term,
                                  last_log_index=len(self.state.log))
            p1 = self.get_vote_from_peers(peer, request)
            peer_votes.append(p1)
            if p1.voted_for == self.state.server.id:
                yay_votes += 1

        vote_responses = peer_votes
        formatted_responses = [
            f"server_id: {vote_response.server_id}, term: {vote_response.term}, voted_for: {vote_response.voted_for}"
            for vote_response in vote_responses]
        print(f"Vote responses from Peers for {self.state.server.id} are: {formatted_responses}")

        if self.has_majority_votes(yay_votes):
            print(f"+++++++++++++++++++++++++++++ {self.state.server.id} has majority votes ++++++++++++++++++++++++++++++++")
            self.to_leader()
        else:
            print(f"------------------------------- {self.state.server.id} does not have majority votes -------------------------------")
            self.to_follower()

    def get_vote_from_peers(self, peer, request):
        vote_response = peer.stub.request_vote(request)
        return vote_response

    def to_leader(self):
        self.election_timer.stop()
        leader = self.transitioner.to_leader(self.state)
        return leader

    def to_follower(self):
        self.election_timer.stop()
        follower = self.transitioner.to_follower(self.state)
        return follower

    # def append_entries(self, request):
    #     print(f"Called append_entries in candidate : {self.state.server_info.id}")
    #     # TODO - check if the request is valid
    #     # Check if current term is greater than the request term
    #     # if request.term < self.state.current_term: - whatever
    #     self.election_timer.reset()
