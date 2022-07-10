import asyncio

import grpc

from learn_raft.stubs import raft_pb2_grpc
from learn_raft.stubs.raft_pb2 import RequestVote
from learn_raft_kvstore.stubs import kvstore_pb2
from learn_raft_kvstore.stubs import kvstore_pb2_grpc
from learn_raft_kvstore.stubs.kvstore_pb2 import STATUS_SUCCESS


class KVStore(kvstore_pb2_grpc.KeyValueStoreServicer):

    def __init__(self, raft_node):
        #FIXME Switch this to raft_node.leader_id
        #The KV store could connect to any node at the beginning and it gets routed to the proper leader
        self.raft_node=raft_node
        #if self.raft_node.leader_id !=

    def init(self):
        #self.raft_node.start()
        # channel = grpc.insecure_channel("localhost:5090")
        # self.leader_client= raft_pb2_grpc.RaftStub(channel)
        pass

    def get(self, request, context):
        #request_vote = RequestVote(server_id=1, term=1, last_log_term=1, last_log_index=1)
        #response, call = self.leader_client.request_vote.with_call(request_vote)
        print("Calling Get")
        key = request.key
        print(f"Key is {key}")
        return kvstore_pb2.GetCommandResponse(found=True, key=key, value ="1 value")

    def set(self, request, context):
        print("Calling Set")
        # request_vote = RequestVote(server_id=1, term=1, last_log_term=1, last_log_index=1)
        # response = self.leader_client.request_vote(request_vote)

        #print(f"REsponse: {response}")

        request_id = request.request_id
        key = request.key
        value = request.value
        print(f"Request: {request_id}, Key: {key}, Value: {value}")
        return kvstore_pb2.SetCommandResponse(request_id=request_id, status=STATUS_SUCCESS)

