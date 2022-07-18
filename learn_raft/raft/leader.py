import datetime

from learn_raft.raft.node_base import NodeBase
from learn_raft.raft.timer import Timer
from learn_raft.raft.transitioner import Transitioner
from learn_raft.stubs.raft_pb2 import AppendEntries, RESULT_SUCCESS, AppendEntriesResponse


class Leader(NodeBase):
    def __init__(self, state):
        super().__init__(state)
        self.start_heartbeat_timer()
        self.start_stepdown_timer()

    def start_heartbeat_timer(self):
        interval = self.state.config['heartbeat_interval']
        print(f"Starting heartbeat timer for {self.state.server.id} at interval {interval} seconds")
        # TODO Need to check if this is the right way to do this. I believe the append_entries would kick in to reset this.
        self.heartbeat_timer = Timer(interval, self.send_heartbeat, self.state.server.id, "leader", "heartbeat")
        self.heartbeat_timer.start()
        print(f"Heartbeat timer started for {self.state.server.id} at {datetime.datetime.now()}")

    def start_stepdown_timer(self):
        interval = self.state.config['step_down_timeout']
        print(f"Starting election timer for {self.state.server.id} at interval {interval} seconds")
        # TODO Need to check if this is the right way to do this. I believe the append_entries would kick in to reset this.
        self.stepdown_timer = Timer(interval, self.stepdown, self.state.server.id, "leader", "stepdown")
        self.stepdown_timer.start()
        print(f"Stepdown timer started for {self.state.server.id} at {datetime.datetime.now()}")

    def send_heartbeat(self):
        # entry = LogEntry(type=1, term=self.state.current_term, index=1, command=str.encode("heartbeat"))
        request = AppendEntries(term=self.state.term,
                                leader_id=self.state.server.id,
                                prev_log_term=1,
                                prev_log_index=1,
                                leader_commit_index=1,
                                entries=[])
        self.append_entries(request)

    def append_entries(self, request):
        if not request.entries:
            print(f"Leader {self.state.server.id} sending heartbeats.")
        else:
            print(f"Leader {self.state.server.id} calling append_entries with payload {request}")

        if not self.state.peer_map:
            print(f"No peers found for {self.state.server.id}")
            self.stepdown_timer.reset()
        else:
            peer_responses = []
            for id, peer in self.state.peer_map.items():
                if self.state.server.id == peer.server.id:
                    continue
                # print(f"Calling append_entries on peer: {peer_tostring(peer)} WITH REQUEST {append_request_tostring(request)}")
                p1 = peer.stub.append_entries(request=request)
                peer_responses.append(p1)

            # For now, just reset the timer
            # yay_responses = [response for response in peer_responses if response.result == RESULT_SUCCESS]
            # yays = len(yay_responses)
            # self.stepdown_timer.reset() #TODO - Uncomment

            # print(f"Append entries responses from Peers for {self.state.server.id} are: {peer_responses}")
            yay_responses = [response for response in peer_responses if response.result == RESULT_SUCCESS]
            yays = len(yay_responses)
            if self.has_majority_votes(yays):
                self.stepdown_timer.reset()
                # print(f"Resetting stepdown_timer after server id {self.state.server.id} received majority votes.")
            else:
                print(f"server id {self.state.server.id} did not receive majority votes. Stepping down as follower")
                self.stepdown_timer.stop()
                self.heartbeat_timer.stop()
                Transitioner.to_follower(self.state)

        # Update cluster manager with new leader
        # print("Updating cluster manager with the new leader")
        self.cluster_manager.update_leader(request)
        return AppendEntriesResponse(result=RESULT_SUCCESS, term=self.state.term, last_log_index=self.state.last_applied_index)

    def stepdown(self):
        self.heartbeat_timer.stop()
        self.stepdown_timer.stop()
        follower = Transitioner.to_follower(self.state)
        return follower
