import json

import grpc
from google.protobuf.json_format import MessageToJson

from learn_raft.raft import server_tostring
from learn_raft.stubs import raft_pb2_grpc, cluster_manager_pb2_grpc, cluster_manager_pb2
from learn_raft.stubs.cluster_manager_pb2 import GetNodeResponse
from learn_raft.stubs.raft_pb2 import AddNodeResponse, RemoveNodeResponse, AddNode, RemoveNode


class ClusterManagerService(cluster_manager_pb2_grpc.ClusterManagerServicer):
    def __init__(self):
        self.cluster_map = {}

    def add_node(self, request, context):
        server_info = request.server
        print(f"Registering Raft Server at {server_tostring(server_info)}")
        if server_info.id in self.cluster_map:
            print(f"----- Server {server_info.id} already registered. Removing and adding the node again.")
            del self.cluster_map[server_info.id]
        stub = self.create_stub(server_info.host, server_info.port)
        self.cluster_map[server_info.id] = (server_info, stub)
        print(f"++++++ Added node {server_info.id} to cluster manager map")
        self.propagate_node_addition()
        self.print_cluster_map()
        # FIXME - This is a hack. We need to analyse the responses from the add_node and remove_node calls and then response
        return AddNodeResponse(result=True)

    def remove_node(self, request, context):
        print(f"De-registering Raft Server node {request.id}")
        if request.id in self.cluster_map:
            print("Removing node from cluster manager map")
            del self.cluster_map[request.id]
        else:
            print("Node not found in cluster manager map. Nothing to do")
        self.propagate_node_removal()
        self.print_cluster_map()
        # FIXME - This is a hack. We need to analyse the responses from the add_node and remove_node calls and then response
        return RemoveNodeResponse(result=True)

    def propagate_node_addition(self):
        for id, (info, stub) in self.cluster_map.items():
            print(f"Propagating node addition to {server_tostring(info)}")
            response = stub.add_node(request=AddNode(server=info))
            value = MessageToJson(response)
            json_value = json.loads(value)
            print("json_value: " + str(json_value))
            print(f"Add node response :{response.result}")

    def propagate_node_removal(self):
        for id, (info, stub) in self.cluster_map.items():
            print(f"Propagating node addition to {server_tostring(info)}")
            stub.add_node(request=RemoveNode(id=id))

    def send_heartbeats(self):
        for server in self.cluster_map.values():
            # TODO
            print(f"Sending heartbeat to {server_tostring(server)}")

    def get_nodes(self, request, context):
        return GetNodeResponse(servers=[info for info, stub in self.cluster_map.values()])

        # def read_config(self, config):
        #     raft_server_configs = config["raft_servers"]
        #     raft_servers = []
        #     for server_config in raft_server_configs:
        #         server = Server(id=int(server_config["id"]), host=server_config["host"], port=int(server_config["port"]))
        #         raft_servers.append(server)
        #     return raft_servers

    def create_stub(self, host, port):
        channel = grpc.insecure_channel(f"{host}:{port}")
        return raft_pb2_grpc.RaftStub(channel)


    def print_cluster_map(self):
        print(f"********************************* Cluster Map ********************************")
        for id, (info, stub) in self.cluster_map.items():
            print(f"Node {server_tostring(info)}")
        print(f"********************************* Cluster Map ********************************")