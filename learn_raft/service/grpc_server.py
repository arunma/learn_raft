from concurrent import futures

import grpc

from learn_raft.raft.raft_node import RaftNode
from learn_raft.service.raft_service import RaftService
from learn_raft.stubs import raft_pb2_grpc
from learn_raft.stubs.raft_pb2 import Server


def start(ports):
    #TODO Convert to aio
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))

    local_port=ports[0]
    peer_ports=ports[1:]
    local_server = Server(host="[::]", port=local_port, server_id=f"localhost:{local_port}")
    peer_servers = [Server(host="[::]", port=port, server_id=f"localhost:{port}") for port in peer_ports]
    raft_node = RaftNode(local_server, peer_servers)
    servicer = RaftService(raft_node)
    raft_pb2_grpc.add_RaftServicer_to_server(servicer, server)

    print(f"Starting Raft Server at {local_server}")

    local_address = f"{local_server.host}:{local_server.port}"
    server.add_insecure_port(local_address)
    server.start()
    server.wait_for_termination()
