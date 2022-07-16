from learn_raft.raft import server_tostring


class Transitioner:
    @classmethod
    def to_candidate(cls, state):
        from learn_raft.raft.candidate import Candidate
        print(f"Node {server_tostring(state.server_info)} about to change to candidate......")
        candidate = Candidate(state)
        candidate.voted_for = None
        print(f"Node {server_tostring(state.server_info)} changed to candidate......")
        return candidate

    def to_leader(self, state):
        from learn_raft.raft.leader import Leader
        print(f"Node {server_tostring(state.server_info)} about to change to leader......")
        leader = Leader(state)
        leader.state.voted_for = state.server_info.id
        print(f"Node {server_tostring(state.server_info)} changed to leader......")
        return leader

    def to_follower(self, state):
        from learn_raft.raft.follower import Follower
        print(f"Node {server_tostring(state.server_info)} about to change to follower......")
        follower = Follower(state)
        follower.voted_for = None
        print(f"Node {server_tostring(state.server_info)} changed to follower......")
        return follower