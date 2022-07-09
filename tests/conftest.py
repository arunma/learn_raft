import grpc_testing
import pytest

from learn_raft.service.GreeterServicer import GreeterServicer
from learn_raft.stubs import raft_pb2

servicers={raft_pb2._GREETER: GreeterServicer()}

@pytest.fixture(scope="function")
def test_server():
    return grpc_testing.server_from_dictionary(servicers, grpc_testing.strict_real_time())