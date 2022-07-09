from concurrent import futures

import grpc

from learn_raft.service.GreeterServicer import GreeterServicer
from learn_raft.stubs import raft_pb2_grpc


def start(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    servicer = GreeterServicer()
    raft_pb2_grpc.add_GreeterServicer_to_server(servicer, server)

    host = "[::]"
    address = f"{host}:{port}"
    print(f"Starting grpc server at {address}")

    server.add_insecure_port(address)
    server.start()
    server.wait_for_termination()
