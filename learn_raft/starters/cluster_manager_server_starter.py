from concurrent import futures

import grpc
from grpc import aio

from learn_raft.service.cluster_manager_service import ClusterManagerService
from learn_raft.stubs import raft_pb2_grpc, cluster_manager_pb2_grpc


class ClusterManagerServerStarter:
    def __init__(self):
        self.cluster_map = {}

    async def start(self, id, host, port, config):
        server = aio.server(futures.ThreadPoolExecutor(max_workers=5))
        servicer = ClusterManagerService()
        cluster_manager_pb2_grpc.add_ClusterManagerServicer_to_server(servicer, server)
        local_address = f"{host}:{port}"
        server.add_insecure_port(local_address)

        await server.start()
        print(f"Cluster Manager listening at {host}:{port}")
        # self.cluster_manager_stub = cluster_manager_pb2_grpc.ClusterManagerStub(aio.insecure_channel(local_address))
        await server.wait_for_termination()

    def create_stub(self, host, port):
        channel = grpc.insecure_channel(f"{host}:{port}")
        return raft_pb2_grpc.RaftStub(channel)
