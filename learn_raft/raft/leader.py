from learn_raft.raft.base_state import BaseState
from learn_raft.raft.state import State


class Leader(BaseState):
    def __init__(self, state):
        super().__init__(state)
    #
    # def append_entries(self, request):
    #     print("Called append_entries in RAFT_NODE")
    #     pass
    #

    def to_follower(self):
        from learn_raft.raft.follower import Follower
        follower = Follower(self.state)
        follower.state.voted_for = None
        return follower

