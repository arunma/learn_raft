from enum import Enum


def server_tostring(server):
    return f"{server.id} --> {server.host}:{server.port}"

def peer_tostring(peer):
    return f"peer_server:{server_tostring(peer.server_info)}, voted_for: {peer.voted_for}, next_index: {peer.next_index}, match_index: {peer.match_index}"

def append_request_tostring(request):
    return f"term: {request.term}, leader_id: {request.leader_id}, prev_log_term: {request.prev_log_term}, prev_log_index: {request.prev_log_index}, leader_commit_index: {request.leader_commit_index}, entries: {request.entries}"

def add_node_tostring(add_node):
    return f"{add_node.server.id}:{add_node.server.host}:{add_node.server.port} -> config {add_node.config}"

def state_tostring(state):
    return f"\n{state.server_info.id} --> {state.server_info.host}:{state.server_info.port}, \ncurrent_term: {state.current_term}, \nvoted_for: {state.voted_for}, \nlog: {state.log}, \npeer_map: {state.peer_map}"
class NodeState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3



