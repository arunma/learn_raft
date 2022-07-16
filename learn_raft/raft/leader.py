import datetime
import threading

from learn_raft.raft import peer_tostring, append_request_tostring
from learn_raft.raft.base_state import NodeBase
from learn_raft.raft.timer import Timer
from learn_raft.stubs.raft_pb2 import AppendEntries, RESULT_SUCCESS


class Leader(NodeBase):
    def __init__(self, state):
        super().__init__(state)
        self.start_heartbeat_timer()
        #self.start_stepdown_timer()

    def start_heartbeat_timer(self):
        interval = self.state.config['heartbeat_interval']
        print(f"Starting heartbeat timer for {self.state.server_info.id} at interval {interval} seconds")
        # TODO Need to check if this is the right way to do this. I believe the append_entries would kick in to reset this.
        self.heartbeat_timer = Timer(interval, self.send_heartbeat, self.state.server_info.id, "leader", "heartbeat")
        self.heartbeat_timer.start()
        print(f"Heartbeat timer started for {self.state.server_info.id} at {datetime.datetime.now()}")

    def start_stepdown_timer(self):
        interval = self.state.config['step_down_timeout']
        print(f"Starting election timer for {self.state.server_info.id} at interval {interval} seconds")
        # TODO Need to check if this is the right way to do this. I believe the append_entries would kick in to reset this.
        self.stepdown_timer = Timer(interval, self.stepdown, self.state.server_info.id, "leader")
        print(f"Stepdown timer started for {self.state.server_info.id} at {datetime.datetime.now()}")

    def send_heartbeat(self):
        # entry = LogEntry(type=1, term=self.state.current_term, index=1, command=str.encode("heartbeat"))
        request = AppendEntries(term=self.state.current_term,
                                leader_id=self.state.server_info.id,
                                prev_log_term=1,
                                prev_log_index=1,
                                leader_commit_index=1,
                                entries=[])
        self.append_entries(request)

    def append_entries(self, request):
        print(f"LEADER : {self.state.server_info.id} calling append_entries with payload {request}")
        if not self.state.peer_map:
            print(f"No peers found for {self.state.server_info.id}")
        else:
            peer_responses = []
            for id, peer in self.state.peer_map.items():
                if self.state.server_info.id == peer.server_info.id:
                    continue
                print(
                    f"Calling append_entries on peer: {peer_tostring(peer)} WITH REQUEST {append_request_tostring(request)}")
                print("peer's stub is: ", peer.stub)
                p1, call = peer.stub.append_entries.with_call(request)
                print(call.trailing_metadata())
                peer_responses.append(p1)

            # For now, just reset the timer
            yay_responses = [response for response in peer_responses if response.result == RESULT_SUCCESS]
            yays = len(yay_responses)
            #self.stepdown_timer.reset() #TODO - Uncomment

            # print(f"Append entries responses from Peers for {self.state.server_info.id} are: {peer_responses}")
            # yay_responses = [response for response in peer_responses if response.result == RESULT_SUCCESS]
            # yays = len(yay_responses)
            # if self.has_majority_votes(yays):
            #     self.reset_heartbeat_timer()
            #     print(f"Resetting heartbeat_timer after server id {self.state.server_info.id} received majority votes.")
            # else:
            #     print(f"server id {self.state.server_info.id} did not receive majority votes. Stepping down as follower")
            #     self.to_follower()

    def stepdown(self):
        self.heartbeat_timer.stop()
        self.stepdown_timer.stop()
        follower = self.transitioner.to_follower(self.state)
        return follower
