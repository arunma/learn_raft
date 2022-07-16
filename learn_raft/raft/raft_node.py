# from learn_raft.raft import NodeState
# from learn_raft.raft.follower import Follower
#
# class RaftNode:
#     def __init__(self, local_server_info, config, node_state=NodeState.FOLLOWER):
#         self.server_info = local_server_info
#         self.node_state = node_state
#         self.config = config
#         self.state = None
#         self.peer_map={}
#
#     async def start(self):
#         pass
#         #self.state.stop()
#         #self.state = Follower.init_with_params(self.server_info, self.config, self.all_servers)
#         #await self.state.init_peers()
#         #self.state.start()
#
#     #Let the node know that the starters configuration has changed
#     def update_cluster_config(self):
#         self.state.update_cluster_config()




# Implementations
# class NodeFunction:
#     def __init__(self, config, server_info, raft_node):
#         self.raft_node = raft_node
#         self.config=config
#         self.server_info=server_info
#
#     def start_election_timer(self):
#         interval_from = self.config['election_timeout_from']
#         interval_to = self.config['election_timeout_to']
#         interval = interval_from + (interval_to - interval_from) * random.random()
#         print(f"Starting election timer for {self.server_info.id} at interval {interval} seconds")
#         self.election_timer=threading.Timer(interval, self.start_election)
#         self.election_timer.start()
#         print(f"Election thread started for {self.server_info.id}")
#
#     def reset_election_timer(self):
#         self.election_timer.reset()
#
#     def stop_election_timer(self):
#         self.election_timer.stop()
#
#     def start_election(self):
#         pass
