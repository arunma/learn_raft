import threading

from learn_raft.raft import peer_tostring, append_request_tostring
from learn_raft.raft.base_state import BaseState
from learn_raft.raft.state import State
from learn_raft.stubs.raft_pb2 import AppendEntries, ResultCode, RESULT_SUCCESS, LogEntry


class Leader(BaseState):
    def __init__(self, state):
        super().__init__(state)
        self.start_heartbeat_timer()
        self.start_stepdown_timer()

    def start_heartbeat_timer(self):
        interval = self.state.config['heartbeat_interval']
        self.heartbeat_timer = threading.Timer(interval, self.send_heartbeat)
        self.heartbeat_timer.start()
        print(f"Heartbeat thread started for {self.state.server_info.id}")

    def send_heartbeat(self):
        #entry = LogEntry(type=1, term=self.state.current_term, index=1, command=str.encode("heartbeat"))
        request = AppendEntries(term=self.state.current_term,
                                leader_id=self.state.server_info.id,
                                prev_log_term=1,
                                prev_log_index=1,
                                leader_commit_index=1,
                                entries=[])
        self.append_entries(request)
        self.start_heartbeat_timer()

    def append_entries(self, request):
        print(f"Called append_entries on LEADER : {self.state.server_info.id} with payload {request}")
        peer_responses = []
        for id, peer in self.state.peer_map.items():
            if self.state.server_info.id == peer.server_info.id:
                continue
            print(f"Calling append_entries on peer: {peer_tostring(peer)} WITH REQUEST {append_request_tostring(request)}")
            print("peer's stub is: ", peer.stub)
            p1, call = peer.stub.append_entries.with_call(request)
            print(call.trailing_metadata())
            peer_responses.append(p1)

        print(f"Append entries responses from Peers for {self.state.server_info.id} are: {peer_responses}")
        yay_responses = [response for response in peer_responses if response.result == RESULT_SUCCESS]
        yays = len(yay_responses)
        if self.has_majority_votes(yays):
            self.reset_heartbeat_timer()
            print(f"Resetting heartbeat_timer after server id {self.state.server_info.id} received majority votes.")
        else:
            print(f"server id {self.state.server_info.id} did not receive majority votes. Stepping down as follower")
            self.to_follower()

    def to_follower(self):
        from learn_raft.raft.follower import Follower
        self.stop_heartbeat_timer()
        self.stop_stepdown_timer()
        follower = Follower(self.state)
        follower.state.voted_for = None
        return follower

    def reset_heartbeat_timer(self):
        self.stop_heartbeat_timer()
        self.start_heartbeat_timer()

    def stop_heartbeat_timer(self):
        self.heartbeat_timer.cancel()

    def start_stepdown_timer(self):
        interval = self.state.config['step_down_timeout']
        self.stepdown_timer = threading.Timer(interval, self.to_follower)
        self.stepdown_timer.start()
        print(f"Stepdown timer thread started for {self.state.server_info.id}")

    def reset_stepdown_timer(self):
        self.stop_stepdown_timer()
        self.start_stepdown_timer()

    def stop_stepdown_timer(self):
        self.stepdown_timer.cancel()
