from learn_raft.raft import server_tostring
from learn_raft.stubs.cluster_manager_pb2 import GetNodes
from learn_raft.stubs.raft_pb2 import AddNode, RESULT_SUCCESS, RequestVote, AppendEntries, GetState, RemoveNode


def test_add_two_nodes(cluster_manager_stub, follower_info_server_1, follower_info_server_2, follower_stub_1, follower_stub_2):
    add_node_response_follower1 = cluster_manager_stub.add_node(AddNode(server=follower_info_server_1))
    add_node_response_follower2 = cluster_manager_stub.add_node(AddNode(server=follower_info_server_2))
    assert add_node_response_follower1.result == RESULT_SUCCESS
    assert add_node_response_follower2.result == RESULT_SUCCESS
    remove_node_response_follower1 = cluster_manager_stub.remove_node(RemoveNode(id=follower_info_server_1.id))
    remove_node_response_follower2 = cluster_manager_stub.remove_node(RemoveNode(id=follower_info_server_2.id))
    assert remove_node_response_follower1.result == RESULT_SUCCESS
    assert remove_node_response_follower2.result == RESULT_SUCCESS



def test_get_nodes_when_two_nodes_are_added(cluster_manager_stub, follower_info_server_1, follower_info_server_2, follower_stub_1, follower_stub_2):
    _ = cluster_manager_stub.add_node(AddNode(server=follower_info_server_1))
    _ = cluster_manager_stub.add_node(AddNode(server=follower_info_server_2))
    get_nodes_response = cluster_manager_stub.get_nodes(GetNodes())
    servers_actual = [server_tostring(server) for server in get_nodes_response.servers]
    servers_expected = ["1 --> 0.0.0.0:2001", "2 --> 0.0.0.0:2002"]
    assert servers_actual == servers_expected
    _ = cluster_manager_stub.remove_node(RemoveNode(id=follower_info_server_1.id))
    _ = cluster_manager_stub.remove_node(RemoveNode(id=follower_info_server_2.id))
