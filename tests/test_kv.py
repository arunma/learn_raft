import unittest

import grpc
import yaml

from learn_raft.stubs.raft_pb2 import Server
from learn_raft_kvstore.stubs import kvstore_pb2
from learn_raft_kvstore.stubs.kvstore_pb2 import GetCommand

def test_kv():
    print("test_base")
    assert 1 == 2
    # service_descriptor=kvstore_pb2._KEYVALUESTORE
    # method_descriptor = service_descriptor.methods_by_name['get']
    # request = GetCommand(key="1")
    #
    # get_method = test_server.invoke_unary_unary(method_descriptor=method_descriptor,
    #                                                   invocation_metadata={},
    #                                                   request=request,
    #                                                   timeout=10)
    #
    # response, metadata, code, details = get_method.termination()
    #
    # assert code == grpc.StatusCode.OK
    # assert response.found == True
    # assert response.key == f"1 key"
    # assert response.value == f"1 value"

def test_read_yaml():
    config_file = open("../learn_raft_kvstore/config/conf.yaml")
    config = yaml.safe_load(config_file)
    raft_server_configs = config["raft_servers"]
    raft_servers=[]
    for server_config in raft_server_configs:
        server = Server(id=int(server_config["id"]), host=server_config["host"], port=int(server_config["port"]))
        raft_servers.append(server)

    kv_server_config = config["kv_server"]
    kv_server = Server(id=int(kv_server_config["id"]), host=kv_server_config["host"], port=int(kv_server_config["port"]))

    assert kv_server.host =='0.0.0.0'
    assert kv_server.port ==8080
    assert kv_server.id ==9999

    assert raft_servers[0].host == '0.0.0.0'
    assert raft_servers[0].port == 5090
    assert raft_servers[0].id == 1

