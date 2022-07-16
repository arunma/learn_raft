from learn_raft.raft import server_tostring
from learn_raft.raft.peer import Peer


class State:

    def __init__(self, server_info, config, cluster_manager_ip):
        self.server_info = server_info
        self.config = config
        self.cluster_manager_ip= cluster_manager_ip

        # Persistent state
        self.log = []
        self.current_term = 0
        self.state_machine = None

        # Volatile state on all servers
        self.commit_index = None
        self.last_applied_index = None

        #self.all_servers = all_servers
        self.peer_map = {}

        self.voted_for = None
        self.election_timer=None

        self.election_timeout_from = self.config['election_timeout_from']
        self.election_timeout_to = self.config['election_timeout_to']

    #TODO Initialize server on Base state
    # async def init_peers(self):
    #     for server in self.all_servers:
    #         if server.id != self.server_info.id and server_tostring(server) not in self.peer_map:
    #             peer = Peer(server)
    #             await peer.start()
    #             self.peer_map[server_tostring(server)] = peer