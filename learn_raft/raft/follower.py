import threading
from random import random

from learn_raft.raft.base_state import BaseState
from learn_raft.raft.candidate import Candidate
from learn_raft.raft.state import State


class Follower(BaseState):

    def __init__(self, state):
        super().__init__(state)
        self.start_election_timer()

    @classmethod
    def init_with_params(cls, local_server_info, config, all_servers):
        state=State(local_server_info, config, all_servers)
        return cls(state)

    def start_election_timer(self):
        interval_from = self.state.config['election_timeout_from']
        interval_to = self.state.config['election_timeout_to']
        interval = interval_from + (interval_to - interval_from) * random()
        print(f"Starting election timer for {self.state.server_info.id} at interval {interval} seconds")
        self.election_timer = threading.Timer(interval, self.start_election)
        self.election_timer.start()
        print(f"Election thread started for {self.state.server_info.id}")

    def reset_election_timer(self):
        self.stop_election_timer()
        self.start_election_timer()

    def stop_election_timer(self):
        self.election_timer.cancel()

    def stop(self):
        # start election.
        # TODO - don't forget to reset the timer after append_entries (heartbeat)
        self.stop_election_timer()

    def start_election(self):
        #TODO - Pass the old state from which the new state could be constructed
        #self.change_state(NodeState.CANDIDATE)
        #For now, just switch to candidate blindly.  We'll need to check for heartbeats at a later point
        self.to_candidate()



    def append_entries(self, request):
        print(f"Called append_entries in follower node : {self.state.server_info.id}")
        #TODO - check if the request is valid
        #Check if current term is greater than the request term
        #if request.term < self.state.current_term: - whatever
        print(f"Resetting election timer for follower : {self.state.server_info.id}")
        #self.reset_election_timer()
        self.stop_election_timer() #FIXME - Stopping for debugging

    def to_candidate(self):
        self.stop_election_timer()
        candidate = Candidate(self.state)
        candidate.voted_for = None
