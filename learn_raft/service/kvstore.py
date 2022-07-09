from learn_raft.stubs import kvstore_pb2
from learn_raft.stubs import kvstore_pb2_grpc
from learn_raft.stubs.kvstore_pb2 import STATUS_SUCCESS


class KVStore(kvstore_pb2_grpc.KeyValueStoreServicer):

    def get(self, request, context):
        print("Calling Get")
        key = request.key
        print(f"Key is {key}")
        return kvstore_pb2.GetCommandResponse(found=True, key="1 key", value ="1 value")

    def set(self, request, context):
        print("Calling Set")
        request_id = request.request_id
        key = request.key
        value = request.value
        print(f"Request: {request_id}, Key: {key}, Value: {value}")
        return kvstore_pb2.SetCommandResponse(request_id=request_id, status=STATUS_SUCCESS)

