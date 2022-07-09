from concurrent import futures

import grpc

from learn_raft.service.kvstore import KVStore
from learn_raft.stubs import kvstore_pb2_grpc


def start(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    servicer = KVStore()
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(servicer, server)

    host = "[::]"
    address = f"{host}:{port}"
    print(f"Starting KV store server at {address}")

    server.add_insecure_port(address)
    server.start()
    server.wait_for_termination()
