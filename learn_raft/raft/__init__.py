from enum import Enum


def server_tostring(server):
    return f"{server.id} --> {server.host}:{server.port}"


def peer_tostring(peer):
    return f"peer_server:{server_tostring(peer.server)}"


def append_request_tostring(request):
    return f"term: {request.term}, " \
           f"leader_id: {request.leader_id}, " \
           f"prev_log_term: {request.prev_log_term}, " \
           f"prev_log_index: {request.prev_log_index}, " \
           f"leader_commit_index: {request.leader_commit_index}, " \
           f"entries: {request.entries}"


def add_node_tostring(add_node):
    return f"{add_node.server.id}:{add_node.server.host}:{add_node.server.port} -> config {add_node.config}"


def state_tostring(state):
    return f"\n{state.server.id} --> {state.server.host}:{state.server.port}, " \
           f"\ncurrent_term: {state.term}, " \
           f"\nvoted_for: {state.voted_for}, " \
           f"\nlog: {state.log}, " \
           f"\npeer_map: {state.peer_map}"


class NodeState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3
