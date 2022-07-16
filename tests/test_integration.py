import asyncio

import grpc
import pytest
import yaml

from learn_raft.starters.raft_server_starter import RaftServerStarter
from learn_raft_kvstore.stubs import kvstore_pb2
from learn_raft_kvstore.stubs.kvstore_pb2 import GetCommand

# @pytest.mark.integration
# def test_kv_integration(integration_server, kv_stub):
#     print(kv_stub)
#     response, call = kv_stub.get.with_call(request=GetCommand(key="KEY"))
#     print(response)


def test_leader_check():
    cluster_manager_ip="0.0.0.0:9999"
    raft_server = RaftServerStarter(cluster_manager_ip)
    config_file = open("../learn_raft_kvstore/config/conf.yaml")
    config = yaml.safe_load(config_file)
    asyncio.run(raft_server.start(9, "0.0.0.0", 5999, config))