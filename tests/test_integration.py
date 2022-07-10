import grpc
import pytest

from learn_raft_kvstore.stubs import kvstore_pb2
from learn_raft_kvstore.stubs.kvstore_pb2 import GetCommand

@pytest.mark.integration
def test_kv_integration(integration_server, kv_stub):
    print(kv_stub)
    response, call = kv_stub.get.with_call(request=GetCommand(key="KEY"))
    print(response)
