import threading
from random import random

from learn_raft.raft.node_base import NodeBase
from learn_raft.raft.state import State
from learn_raft.raft.timer import Timer
from learn_raft.stubs.raft_pb2 import AppendEntriesResponse, ResultCode, RESULT_FAILURE, RESULT_SUCCESS


class Follower(NodeBase):
    def __init__(self, state):
        super().__init__(state)
        self.start_election_timer()

    def start_election_timer(self):
        interval = self.state.election_timeout_from + (self.state.election_timeout_to - self.state.election_timeout_from) * random()
        print(f"Starting election timer for {self.state.server.id} at interval {interval} seconds")
        self.election_timer = Timer(interval, self.start_election, self.state.server.id, "follower")
        self.election_timer.start()
        #self.start_election()
        print(f"Election thread started for {self.state.server.id}")

    @classmethod
    def init_with_info(cls, server_info, config, cluster_manager_ip):
        print("INIT INFO called in Follower")
        state = State(server_info, config, cluster_manager_ip)
        return cls(state)

    def start_election(self):
        # TODO - Pass the old state from which the new state could be constructed
        # self.change_state(NodeState.CANDIDATE)
        # For now, just switch to candidate blindly.  We'll need to check for heartbeats at a later point
        if not self.state.voted_for:
            print("Leader is not known. Starting election")
            self.to_candidate()

    def append_entries(self, request):
        print(f"Received append_entries in follower : {self.state.server.id} from leader: {request.leader_id}")
        # TODO - check if the request is valid
        # Check if current term is greater than the request term
        # if request.term < self.state.current_term: - whatever
        if request.term < self.state.current_term:
            print(f"Request term {request.term} is less than current term {self.state.current_term}. Converting to CANDIDATE")
            self.to_candidate()
            return AppendEntriesResponse(result=RESULT_FAILURE, term=self.state.current_term, last_log_index=self.state.last_applied_index)
        else:
            leader_id=request.leader_id
            leader_term=request.term
            self.state.voted_for=leader_id
            #print(f"Resetting election timer for follower : {self.state.server.id}")
            self.election_timer.reset()
            return AppendEntriesResponse(result=RESULT_SUCCESS, term=self.state.current_term, last_log_index=self.state.last_applied_index)


    def to_candidate(self):
        self.election_timer.stop()
        self.transitioner.to_candidate(self.state)
