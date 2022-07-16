from concurrent import futures
from multiprocessing import Process

import grpc

from learn_raft.stubs import cluster_manager_pb2_grpc
from learn_raft_kvstore.service.kvstore import KVStore
from learn_raft_kvstore.stubs import kvstore_pb2_grpc


class KVServer:
    def __init__(self, cluster_manager_ip):
        self.cluster_manager_ip = cluster_manager_ip
        self.raft_cluster_manager_channel = grpc.insecure_channel(cluster_manager_ip)
        self.raft_cluster_manager = cluster_manager_pb2_grpc.ClusterManagerStub(self.raft_cluster_manager_channel)

    # async def add_raft_node(self, id, host, port, config):
    #     server_info = Server(id=id, host=host, port=port)
    #     server = aio.server(futures.ThreadPoolExecutor(max_workers=5))
    #     raft_node = RaftNode(server_info, config)
    #     servicer = RaftService(raft_node) #TODO - Remove this redirection
    #     raft_pb2_grpc.add_RaftServicer_to_server(servicer, server)
    #     print(f"Starting Raft Server at {server_info}")
    #     local_address = f"{server_info.host}:{server_info.port}"
    #     server.add_insecure_port(local_address)
    #     await server.start()
    #     await raft_node.start()
    #     self.register_raft_node(server_info)
    #     await server.wait_for_termination()
    #
    #     # Wrap this as a decorator
    # def register_raft_node(self, server_info):
    #     print(f"Registering node {server_tostring(server_info)}")
    #     add_node_request = AddNode(server=server_info)
    #     raft_cluster_manager_channel = grpc.insecure_channel(self.cluster_manager_ip)
    #     raft_cluster_manager = cluster_manager_pb2_grpc.ClusterManagerStub(raft_cluster_manager_channel)
    #     print(f"About to call starters manager add_node {add_node_tostring(add_node_request)}")
    #     raft_cluster_manager.add_node(add_node_request)
    #     print("Done calling starters manager add_node")

    def add_kv_node(self, id, host, port, config):
        process = None
        try:
            process = Process(target=self.kv_init, args=(id, host, port, config))
            process.start()
        finally:
            if process and process.is_alive():
                print(f"Terminating {process}")
                process.terminate()
                process.join()

    def kv_init(self, id, host, port, config_file):
        all_servers = self.raft_cluster_manager.get_nodes()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        servicer = KVStore(self.raft_cluster_manager)#This might not work, since we are trying to serialize an entire stub
        kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(servicer, server)
        print(f"Starting  KV store server at {id}:{host}:{port}")
        local_address = f"{host}:{port}"
        server.add_insecure_port(local_address)
        server.start()
        server.wait_for_termination()