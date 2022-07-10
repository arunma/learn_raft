import asyncio

import grpc
import grpc_testing
import pytest
import yaml

from learn_raft.stubs.raft_pb2 import Server
from learn_raft_kvstore.service import kv_grpc_server
from learn_raft_kvstore.service.kvstore import KVStore
from learn_raft_kvstore.stubs import kvstore_pb2

# servicers={kvstore_pb2._KEYVALUESTORE: KVStore()}
#
# @pytest.fixture(scope="function")
# def test_server():
#     return grpc_testing.server_from_dictionary(servicers, grpc_testing.strict_real_time())
from learn_raft_kvstore.stubs.kvstore_pb2_grpc import KeyValueStoreStub


@pytest.fixture(scope="module")
def integration_server(config):
    asyncio.run(kv_grpc_server.start(config))


@pytest.fixture(scope="module")
def kv_stub(kv_server):
    kv_address=f"{kv_server.host}:{kv_server.port}"
    channel = grpc.insecure_channel(kv_address)
    return KeyValueStoreStub(channel)

@pytest.fixture(scope="module")
def config():
    config_file = open("../learn_raft_kvstore/config/conf.yaml")
    config = yaml.safe_load(config_file)
    return config

@pytest.fixture(scope="module")
def raft_servers(config):
    raft_server_configs = config["raft_servers"]
    raft_servers = []
    for server_config in raft_server_configs:
        server = Server(id=int(server_config["id"]), host=server_config["host"], port=int(server_config["port"]))
        raft_servers.append(server)
    return raft_servers

@pytest.fixture(scope="module")
def kv_server(config):
    kv_server_config = config["kv_server"]
    kv_server = Server(id=int(kv_server_config["id"]), host=kv_server_config["host"], port=int(kv_server_config["port"]))
    return kv_server

async def check_socket(host, port):
    fut = asyncio.open_connection(host, port)
    await asyncio.wait_for(fut, timeout=3)
