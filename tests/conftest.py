from concurrent import futures
from pathlib import Path

import grpc
import pytest
import yaml

from learn_raft.raft.follower import Follower
from learn_raft.raft.transitioner import Transitioner
from learn_raft.service.cluster_manager_service import ClusterManagerService
from learn_raft.service.raft_service import RaftService
from learn_raft.stubs import cluster_manager_pb2_grpc, raft_pb2_grpc
from learn_raft.stubs.raft_pb2 import Server


@pytest.fixture(scope="session")
def monkeypatch():
    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope="session")
def base_path() -> Path:
    return Path(__file__).parent


@pytest.fixture(scope="module")
def config(base_path, monkeypatch):
    monkeypatch.chdir(base_path)
    config_file = open("../learn_raft_kvstore/config/conf.yaml")
    config = yaml.safe_load(config_file)
    return config


@pytest.fixture(scope="module")
def cluster_manager_address():
    return "0.0.0.0:2222"


# Leader
@pytest.fixture(scope="module")
def leader_info_server_1():
    return Server(id=0, host="0.0.0.0", port=2000)


# Followers
@pytest.fixture(scope="module")
def follower_info_server_1():
    return Server(id=1, host="0.0.0.0", port=2001)


@pytest.fixture(scope="module")
def follower_info_server_2():
    return Server(id=2, host="0.0.0.0", port=2002)


# Candidate 1
@pytest.fixture(scope="module")
def candidate_info_server_1():
    return Server(id=3, host="0.0.0.0", port=2003)


# Candidate 2
@pytest.fixture(scope="module")
def candidate_info_server_2():
    return Server(id=4, host="0.0.0.0", port=2004)


@pytest.fixture(scope="module")
def cluster_manager_server(cluster_manager_address):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    servicer = ClusterManagerService()
    cluster_manager_pb2_grpc.add_ClusterManagerServicer_to_server(servicer, server)
    server.add_insecure_port(cluster_manager_address)
    server.start()
    yield server
    server.stop(grace=None)


@pytest.fixture(scope="module")
def cluster_manager_stub(cluster_manager_server, cluster_manager_address):
    channel = grpc.insecure_channel(cluster_manager_address)
    return cluster_manager_pb2_grpc.ClusterManagerStub(channel)


def build_server(server_info, servicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    raft_pb2_grpc.add_RaftServicer_to_server(servicer, server)
    server.add_insecure_port(f"{server_info.host}:{server_info.port}")
    server.start()
    yield server
    server.stop(grace=None)


@pytest.fixture(scope="module")
def follower_server_1(follower_info_server_1, config, cluster_manager_address):
    raft_node = Follower.init_with_info(follower_info_server_1, config, cluster_manager_address)
    servicer = RaftService(raft_node)
    yield from build_server(follower_info_server_1, servicer)


@pytest.fixture(scope="module")
def follower_stub_1(follower_server_1, follower_info_server_1):
    channel = grpc.insecure_channel(f"{follower_info_server_1.host}:{follower_info_server_1.port}")
    return raft_pb2_grpc.RaftStub(channel)


@pytest.fixture(scope="module")
def follower_server_2(follower_info_server_2, config, cluster_manager_address):
    raft_node = Follower.init_with_info(follower_info_server_2, config, cluster_manager_address)
    servicer = RaftService(raft_node)
    yield from build_server(follower_info_server_2, servicer)


@pytest.fixture(scope="module")
def follower_stub_2(follower_server_2, follower_info_server_2):
    channel = grpc.insecure_channel(f"{follower_info_server_2.host}:{follower_info_server_2.port}")
    return raft_pb2_grpc.RaftStub(channel)


# Leader
@pytest.fixture(scope="module")
def leader_server_1(leader_info_server_1, config, cluster_manager_address):
    raft_node = Follower.init_with_info(leader_info_server_1, config, cluster_manager_address)
    leader_node = Transitioner.to_leader(raft_node.state)
    servicer = RaftService(leader_node)
    yield from build_server(leader_info_server_1, servicer)


@pytest.fixture(scope="module")
def leader_stub_1(leader_server_1, leader_info_server_1):
    channel = grpc.insecure_channel(f"{leader_info_server_1.host}:{leader_info_server_1.port}")
    return raft_pb2_grpc.RaftStub(channel)


@pytest.fixture(scope="module")
def candidate_server_1(candidate_info_server_1, config, cluster_manager_address):
    raft_node = Follower.init_with_info(candidate_info_server_1, config, cluster_manager_address)
    candidate_node = Transitioner.to_candidate(raft_node.state)
    servicer = RaftService(candidate_node)
    yield from build_server(candidate_info_server_1, servicer)


@pytest.fixture(scope="module")
def candidate_stub_1(candidate_server_1, candidate_info_server_1):
    channel = grpc.insecure_channel(f"{candidate_info_server_1.host}:{candidate_info_server_1.port}")
    return raft_pb2_grpc.RaftStub(channel)


@pytest.fixture(scope="module")
def candidate_server_2(candidate_info_server_2, config, cluster_manager_address):
    raft_node = Follower.init_with_info(candidate_info_server_2, config, cluster_manager_address)
    candidate_node = Transitioner.to_candidate(raft_node.state)
    servicer = RaftService(candidate_node)
    yield from build_server(candidate_info_server_2, servicer)


@pytest.fixture(scope="module")
def candidate_stub_2(candidate_server_2, candidate_info_server_2):
    channel = grpc.insecure_channel(f"{candidate_info_server_2.host}:{candidate_info_server_2.port}")
    return raft_pb2_grpc.RaftStub(channel)


# servicers={kvstore_pb2._KEYVALUESTORE: KVStore()}
#
# @pytest.fixture(scope="function")
# def test_server():
#     return grpc_testing.server_from_dictionary(servicers, grpc_testing.strict_real_time())
# from learn_raft_kvstore.stubs.kvstore_pb2_grpc import KeyValueStoreStub
#
#
# @pytest.fixture(scope="module")
# def integration_server(config):
#     asyncio.run(kv_grpc_server.start(config))
#
#
# @pytest.fixture(scope="module")
# def kv_stub(kv_server):
#     kv_address=f"{kv_server.host}:{kv_server.port}"
#     channel = grpc.insecure_channel(kv_address)
#     return KeyValueStoreStub(channel)
#

#
# @pytest.fixture(scope="module")
# def raft_servers(config):
#     raft_server_configs = config["raft_servers"]
#     raft_servers = []
#     for server_config in raft_server_configs:
#         server = Server(id=int(server_config["id"]), host=server_config["host"], port=int(server_config["port"]))
#         raft_servers.append(server)
#     return raft_servers
#
# @pytest.fixture(scope="module")
# def kv_server(config):
#     kv_server_config = config["kv_server"]
#     kv_server = Server(id=int(kv_server_config["id"]), host=kv_server_config["host"], port=int(kv_server_config["port"]))
#     return kv_server
#
# async def check_socket(host, port):
#     fut = asyncio.open_connection(host, port)
#     await asyncio.wait_for(fut, timeout=3)
