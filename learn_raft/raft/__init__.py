def server_tostring(server):
    return f"{server.id}:{server.host}:{server.port}"

def peer_tostring(peer):
    return f"peer_server:{server_tostring(peer.server)}, vote_granted: {peer.vote_granted}, next_index: {peer.next_index}, match_index: {peer.match_index}"