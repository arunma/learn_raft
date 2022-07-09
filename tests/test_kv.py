import grpc

from learn_raft.stubs import kvstore_pb2
from learn_raft.stubs.kvstore_pb2 import GetCommand


def test_base(test_server):
    service_descriptor=kvstore_pb2._KEYVALUESTORE
    method_descriptor = service_descriptor.methods_by_name['get']
    request = GetCommand(key="1")

    get_method = test_server.invoke_unary_unary(method_descriptor=method_descriptor,
                                                      invocation_metadata={},
                                                      request=request,
                                                      timeout=10)

    response, metadata, code, details = get_method.termination()

    assert code == grpc.StatusCode.OK
    assert response.found == True
    assert response.key == f"1 key"
    assert response.value == f"1 value"


