# import asyncio
# from concurrent import futures
# from multiprocessing import Process
#
# import grpc
# from grpc import aio
#
# from learn_raft.raft.raft_node import RaftNode
# from learn_raft.starters.cluster_manager_server_starter import ClusterManager
# from learn_raft.service.raft_service import RaftService
# from learn_raft.stubs import raft_pb2_grpc, cluster_manager_pb2_grpc
# from learn_raft.stubs.cluster_manager_pb2 import AddNode
# from learn_raft.stubs.raft_pb2 import Server
# from learn_raft_kvstore.service.kvstore import KVStore
# from learn_raft_kvstore.stubs import kvstore_pb2_grpc

# class KVServer:
#
#
#
#     def peer_init(server_id, config_file):
#         asyncio.run(start_raft_server(server_id, config_file))

# async def start_raft_server(server_id, config):
#     all_servers = read_config(config)
#     peer_map = {server.id: server for server in all_servers}
#     local_server = peer_map[server_id]
#     server = aio.server(futures.ThreadPoolExecutor(max_workers=5))
#     raft_node = RaftNode(local_server, config, all_servers)
#     servicer = RaftService(raft_node)
#     raft_pb2_grpc.add_RaftServicer_to_server(servicer, server)
#     print(f"Starting Raft Server at {local_server}")
#     local_address = f"{local_server.host}:{local_server.port}"
#     server.add_insecure_port(local_address)
#
#     await server.start()
#     # Modify raft_node init to filter only for non local server
#     await raft_node.start()
#     await server.wait_for_termination()
#
# def read_config(config):
#     raft_server_configs = config["raft_servers"]
#     raft_servers = []
#     for server_config in raft_server_configs:
#         server = Server(id=int(server_config["id"]), host=server_config["host"], port=int(server_config["port"]))
#         raft_servers.append(server)
#     return raft_servers
