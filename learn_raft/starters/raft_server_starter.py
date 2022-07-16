from concurrent import futures

import grpc
from grpc import aio

from learn_raft.raft import server_tostring, add_node_tostring
from learn_raft.raft.follower import Follower
from learn_raft.service.raft_service import RaftService
from learn_raft.stubs import cluster_manager_pb2_grpc, raft_pb2_grpc
from learn_raft.stubs.raft_pb2 import Server, AddNode


class RaftServerStarter:
    def __init__(self, cluster_manager_ip):
        self.cluster_manager_ip = cluster_manager_ip
        # self.raft_cluster_manager_channel = grpc.insecure_channel(cluster_manager_ip)
        # self.raft_cluster_manager = cluster_manager_pb2_grpc.ClusterManagerStub(self.raft_cluster_manager_channel)

    async def start(self, id, host, port, config):
        server_info = Server(id=id, host=host, port=port)
        server = aio.server(futures.ThreadPoolExecutor(max_workers=5))
        #raft_node = RaftNode(server_info, config)
        raft_node = Follower.init_with_info(server_info, config, self.cluster_manager_ip)
        servicer = RaftService(raft_node) #TODO - Remove this redirection
        raft_pb2_grpc.add_RaftServicer_to_server(servicer, server)
        print(f"Starting Raft Server at {server_info}")
        local_address = f"{server_info.host}:{server_info.port}"
        server.add_insecure_port(local_address)
        await server.start()
        #await raft_node.start()
        self.register_raft_node(server_info)
        await server.wait_for_termination()

        # Wrap this as a decorator
    def register_raft_node(self, server_info):
        print(f"Registering node {server_tostring(server_info)}")
        add_node_request = AddNode(server=server_info)
        raft_cluster_manager_channel = grpc.insecure_channel(self.cluster_manager_ip)
        raft_cluster_manager = cluster_manager_pb2_grpc.ClusterManagerStub(raft_cluster_manager_channel)
        print(f"About to call cluster manager add_node {add_node_tostring(add_node_request)}")
        raft_cluster_manager.add_node(add_node_request)
        print("Done calling cluster manager add_node")