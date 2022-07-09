import grpc_testing
import pytest

from learn_raft.service.kvstore import KVStore
from learn_raft.stubs import kvstore_pb2

servicers={kvstore_pb2._KEYVALUESTORE: KVStore()}

@pytest.fixture(scope="function")
def test_server():
    return grpc_testing.server_from_dictionary(servicers, grpc_testing.strict_real_time())