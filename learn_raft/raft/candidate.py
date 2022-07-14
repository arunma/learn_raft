import threading
from random import random

from learn_raft.raft.base_state import BaseState
from learn_raft.raft.leader import Leader
from learn_raft.raft.state import State
from learn_raft.stubs.raft_pb2 import RequestVote, RequestVoteResponse


class Candidate(BaseState):
    def __init__(self, state):
        super().__init__(state)
        self.start_election_timer()

    def start_election_timer(self):
        interval_from = self.state.config['election_timeout_from']
        interval_to = self.state.config['election_timeout_to']
        interval = interval_from + (interval_to - interval_from) * random()
        print(f"Starting election timer for {self.state.server_info.id} at interval {interval} seconds")
        self.election_timer = threading.Timer(interval, self.start_election)
        self.election_timer.start()
        print(f"Election thread started for {self.state.server_info.id}")

    def start_election(self):
        print(f"Called start_election in RAFT_NODE: {self.state.server_info.id}")
        peer_votes = []
        print(f"Peer map items : {self.state.peer_map.items()}")
        yay_votes=0
        #Vote for self
        if not self.voted_for:
            yay_votes+=1
            self.voted_for = self.state.server_info.id

        #Gather votes
        for id, peer in self.state.peer_map.items():
            if peer.server_info.id == self.state.server_info.id:
                continue
            next_term = self.state.current_term + 1
            request = RequestVote(server_id=self.state.server_info.id, term=next_term, last_log_term=self.state.current_term,
                                  last_log_index=len(self.state.log))
            p1 = self.get_vote_from_peers(peer, request)
            peer_votes.append(p1)
            if p1.voted_for==self.state.server_info.id:
                yay_votes+=1

        vote_responses = peer_votes
        formatted_responses =[f"server_id: {vote_response.server_id}, term: {vote_response.term}, voted_for: {vote_response.voted_for}" for vote_response in vote_responses]
        print(f"Vote responses from Peers for {self.state.server_info.id} are: {formatted_responses}")

        if self.has_majority_votes(yay_votes):
            print(f"+++++++++++++++++++++++++++++ {self.state.server_info.id} has majority votes ++++++++++++++++++++++++++++++++")
            self.state = self.to_leader()
        else:
            #print(f"------------------------------- {self.state.server_info.id} does not have majority votes -------------------------------")
            self.state = self.to_follower()

    def get_vote_from_peers(self, peer, request):
        vote_response = peer.stub.request_vote(request)
        return vote_response

    def reset_election_timer(self):
        print(f"Resetting election timer for candidate : {self.state.server_info.id}")
        self.stop_election_timer()
        self.start_election_timer()

    def stop_election_timer(self):
        self.election_timer.cancel()

    def to_leader(self):
        self.stop_election_timer()
        leader = Leader(self.state)
        leader.state.voted_for = self.state.server_info.id
        return leader

    def to_follower(self):
        from learn_raft.raft.follower import Follower
        self.stop_election_timer()
        follower = Follower(self.state)
        follower.state.voted_for = None
        return follower


    def append_entries(self, request):
        print(f"Called append_entries in candidate : {self.state.server_info.id}")
        #TODO - check if the request is valid
        #Check if current term is greater than the request term
        #if request.term < self.state.current_term: - whatever
        self.reset_election_timer()
