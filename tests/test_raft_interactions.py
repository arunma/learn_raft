from learn_raft.raft import server_tostring
from learn_raft.stubs.cluster_manager_pb2 import GetNodes
from learn_raft.stubs.raft_pb2 import AddNode, RESULT_SUCCESS, RequestVote, AppendEntries, GetState

def test_leader_sending_heartbeat(cluster_manager_stub, leader_info_server_1, follower_info_server_2, leader_stub_1, follower_stub_2):
    _ = cluster_manager_stub.add_node(AddNode(server=leader_info_server_1))
    _ = cluster_manager_stub.add_node(AddNode(server=follower_info_server_2))
    append_entry = AppendEntries(term=1, leader_id=leader_info_server_1.id, prev_log_term=1, prev_log_index=1, leader_commit_index=1, entries=[])
    _ = leader_stub_1.append_entries(append_entry)
    get_nodes_response = cluster_manager_stub.get_nodes(GetNodes())
    servers_actual = [server_tostring(server) for server in get_nodes_response.servers]
    servers_expected = ['0 --> 0.0.0.0:2000', '2 --> 0.0.0.0:2002']
    assert servers_actual == servers_expected
    #Heartbeat must update the cluster manager too
    assert get_nodes_response.leader_id == leader_info_server_1.id

def test_node_states_when_two_nodes_are_added(cluster_manager_stub,
                                              leader_info_server_1, follower_info_server_2,
                                              leader_stub_1, follower_stub_2):
    _ = cluster_manager_stub.add_node(AddNode(server=leader_info_server_1))
    _ = cluster_manager_stub.add_node(AddNode(server=follower_info_server_2))
    # Make an initial append entry
    append_entry = AppendEntries(term=1, leader_id=leader_info_server_1.id, prev_log_term=1, prev_log_index=1, leader_commit_index=1, entries=[])
    _ = leader_stub_1.append_entries(append_entry)
    # Get states
    leader_state = leader_stub_1.get_state(GetState())
    follower_state = follower_stub_2.get_state(GetState())

    # Term
    assert leader_state.term == 1
    assert follower_state.term == 1
    # voted_for
    assert leader_state.voted_for == 0
    assert follower_state.voted_for == 0
    # peers
    leader_expected = ['2 --> 0.0.0.0:2002']
    follower_expected = ['0 --> 0.0.0.0:2000']
    leader_actual = [server_tostring(server) for server in leader_state.peers]
    follower_actual = [server_tostring(server) for server in follower_state.peers]
    assert leader_actual == leader_expected
    assert follower_actual == follower_expected


def test_add_node_one_leader_one_follower(cluster_manager_stub, candidate_info_server_1, candidate_stub_1, follower_info_server_2, follower_stub_2):
    add_node_response_candidate = cluster_manager_stub.add_node(AddNode(server=candidate_info_server_1))
    add_node_response_follower1 = cluster_manager_stub.add_node(AddNode(server=follower_info_server_2))

    vote_reponse = candidate_stub_1.request_vote(request=RequestVote(server_id=1, term=1, last_log_term=1, last_log_index=1))
    print(vote_reponse)
