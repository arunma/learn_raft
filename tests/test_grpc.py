import grpc

from learn_raft.stubs import raft_pb2
from learn_raft.stubs.raft_pb2 import HelloRequest


def test_base(test_server):
    name = "ARUN"
    #service_descriptor=raft_pb2.DESCRIPTOR.services_by_name['Greeter']
    service_descriptor=raft_pb2._GREETER

    method_descriptor = service_descriptor.methods_by_name['say_hello']
    request = HelloRequest(name=name)

    say_hello_method = test_server.invoke_unary_unary(method_descriptor=method_descriptor,
                                                      invocation_metadata={},
                                                      request=request,
                                                      timeout=10)

    response, metadata, code, details = say_hello_method.termination()

    assert code == grpc.StatusCode.OK
    assert response.message == f"HELLO {name}"


