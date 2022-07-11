import asyncio
import time
from concurrent import futures
from multiprocessing import Process

import grpc
import yaml
from grpc import aio

from learn_raft.raft.raft_node import RaftNode
from learn_raft.service.raft_service import RaftService
from learn_raft.stubs import raft_pb2_grpc
from learn_raft.stubs.raft_pb2 import Server
from learn_raft_kvstore.service.kvstore import KVStore
from learn_raft_kvstore.stubs import kvstore_pb2_grpc

async def start(config):
    processes = []

    raft_servers = read_config(config)
    # server = await start_kv_server(raft_servers)
    local_server = raft_servers[0]
    peer_servers = raft_servers[1:]
    try:
        process = Process(target=kv_init, args=(local_server.id, config))
        process.start()
        processes.append(process)

        for peer_server in peer_servers:
            process = Process(target=peer_init, args=(peer_server.id, config))
            process.start()
            processes.append(process)

        while processes:
            for process in processes:
                process.join()
                #processes.remove(process)
    finally:
        for process in processes:
            if process.is_alive():
                print(f"Terminating {process}")
                process.terminate()
                process.join()


def kv_init(server_id, config_file):
    asyncio.run(start_kv_server(server_id, config_file))


async def start_kv_server(server_id, config):
    all_servers = read_config(config)
    peer_map = {server.id: server for server in all_servers}
    local_server = peer_map[server_id]
    server = aio.server(futures.ThreadPoolExecutor(max_workers=5))
    raft_node = RaftNode(local_server, config, all_servers)
    servicer = RaftService(raft_node)
    raft_pb2_grpc.add_RaftServicer_to_server(servicer, server)
    servicer = KVStore(raft_node)
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(servicer, server)
    print(f"Starting Raft Server and  KV store server at {local_server}")
    local_address = f"{local_server.host}:{local_server.port}"
    server.add_insecure_port(local_address)
    await server.start()
    await raft_node.start()
    await server.wait_for_termination()
    # return server


def peer_init(server_id, config_file):
    asyncio.run(start_raft_server(server_id, config_file))


async def start_raft_server(server_id, config):
    all_servers = read_config(config)
    peer_map = {server.id: server for server in all_servers}
    local_server = peer_map[server_id]
    server = aio.server(futures.ThreadPoolExecutor(max_workers=5))
    raft_node = RaftNode(local_server, config, all_servers)
    servicer = RaftService(raft_node)
    raft_pb2_grpc.add_RaftServicer_to_server(servicer, server)
    print(f"Starting Raft Server at {local_server}")
    local_address = f"{local_server.host}:{local_server.port}"
    server.add_insecure_port(local_address)

    await server.start()
    # Modify raft_node init to filter only for non local server
    await raft_node.start()
    await server.wait_for_termination()



def read_config(config):
    raft_server_configs = config["raft_servers"]
    raft_servers = []
    for server_config in raft_server_configs:
        server = Server(id=int(server_config["id"]), host=server_config["host"], port=int(server_config["port"]))
        raft_servers.append(server)
    return raft_servers
