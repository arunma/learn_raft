import asyncio
import json

import grpc
from google.protobuf.json_format import MessageToJson

from learn_raft.raft import server_tostring
from learn_raft.stubs import raft_pb2_grpc, cluster_manager_pb2_grpc
from learn_raft.stubs.cluster_manager_pb2 import GetNodesResponse
from learn_raft.stubs.raft_pb2 import AddNodeResponse, RemoveNodeResponse, AddNode, RemoveNode, AppendEntriesResponse, RESULT_SUCCESS


class ClusterManagerService(cluster_manager_pb2_grpc.ClusterManagerServicer):
    def __init__(self):
        self.cluster_map = {}
        self.cluster_leader = None

    def add_node(self, request, context):
        add_candidate_info = request.server
        print(f"Registering Raft Server at {server_tostring(add_candidate_info)}")
        if add_candidate_info.id in self.cluster_map:
            print(f"----- Server {add_candidate_info.id} already registered. Removing and adding the node again.")
            del self.cluster_map[add_candidate_info.id]
        add_candidate_stub = self.create_stub(add_candidate_info.host, add_candidate_info.port)
        self.cluster_map[add_candidate_info.id] = (add_candidate_info, add_candidate_stub)
        print(f"++++++ Added node {add_candidate_info.id} to cluster manager map")
        # self.print_cluster_map()
        asyncio.run(self.propagate_node_addition(add_candidate_info))  # FIXME - Check if all the responses are good
        # FIXME - This is a hack. We need to analyse the responses from the add_node and remove_node calls and then response

        print(f"Attemping to refresh node {add_candidate_info.id} with older nodes in the cluster {self.cluster_map.keys()}")
        # Add existing nodes as peers to the new node
        for id, (info, _) in self.cluster_map.items():
            print("Currently adding node " + str(id) + " as a peer to node " + str(add_candidate_info.id))
            if id != add_candidate_info.id:
                print(f"Adding node {server_tostring(info)} as peer to {server_tostring(add_candidate_info)}")
                response = add_candidate_stub.add_node(AddNode(server=info))
                print(f"Add node response :{response.result == RESULT_SUCCESS}")

        self.print_cluster_map()
        return AddNodeResponse(result=RESULT_SUCCESS)

    def remove_node(self, request, context):
        print(f"De-registering Raft Server node {request.id}")
        if request.id in self.cluster_map:
            print("Removing node from cluster manager map")
            del self.cluster_map[request.id]
        else:
            print("Node not found in cluster manager map. Nothing to do")
        # self.print_cluster_map()
        if self.cluster_leader == request.id:
            self.cluster_leader = None

        self.propagate_node_removal(request.id)
        self.print_cluster_map()
        # FIXME - This is a hack. We need to analyse the responses from the add_node and remove_node calls and then response
        return RemoveNodeResponse(result=True)

    def update_leader(self, request, context):
        if not self.cluster_leader or self.cluster_leader != request.leader_id:
            self.cluster_leader = request.leader_id
            print(f"New leader elected. Updated leader to {request.leader_id}")
            self.print_cluster_map()
        # FIXME - This is a hack. We need to analyse the responses from the add_node and remove_node calls and then response
        return AppendEntriesResponse(result=RESULT_SUCCESS, term=request.term, last_log_index=request.prev_log_index)

    async def propagate_node_addition(self, add_candidate):
        responses = []
        for id, (info, stub) in self.cluster_map.items():
            if id != add_candidate.id:
                print(f"Propagating node {server_tostring(add_candidate)} addition to {server_tostring(info)}")
                response = stub.add_node(request=AddNode(server=add_candidate))
                responses.append(response)
                value = MessageToJson(response)
                json_value = json.loads(value)
                print("json_value: " + str(json_value))
                print(f"Add node response :{response.result}")
            else:
                print(f"Not propagating node {server_tostring(add_candidate)} addition to {server_tostring(info)}")
        # self.print_cluster_map()
        return responses

    def propagate_node_removal(self, remove_candidate):
        for id, (info, stub) in self.cluster_map.items():
            print(f"Propagating node removal of {remove_candidate} to {server_tostring(info)}")
            stub.remove_node(request=RemoveNode(id=remove_candidate))

    def send_heartbeats(self):
        for server in self.cluster_map.values():
            # TODO
            print(f"Sending heartbeat to {server_tostring(server)}")

    def get_nodes(self, request, context):
        return GetNodesResponse(servers=[info for info, stub in self.cluster_map.values()], leader_id=self.cluster_leader)

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
        print("********************************* Cluster Map ********************************")
        for id, (info, stub) in self.cluster_map.items():
            if self.cluster_leader == id:
                print(f"Node {server_tostring(info)} --> Leader")
            else:
                print(f"Node {server_tostring(info)}")
        print("********************************* Cluster Map ********************************")
