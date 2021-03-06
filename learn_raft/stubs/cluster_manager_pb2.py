# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cluster_manager.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import learn_raft.stubs.raft_pb2 as raft__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x15\x63luster_manager.proto\x12\nlearn_raft\x1a\nraft.proto"\n\n\x08GetNodes"J\n\x10GetNodesResponse\x12#\n\x07servers\x18\x01 \x03(\x0b\x32\x12.learn_raft.Server\x12\x11\n\tleader_id\x18\x02 \x01(\r"\x0b\n\tHeartBeat"\x13\n\x11HeartBeatResponse2\xad\x02\n\x0e\x43lusterManager\x12>\n\x08\x61\x64\x64_node\x12\x13.learn_raft.AddNode\x1a\x1b.learn_raft.AddNodeResponse"\x00\x12G\n\x0bremove_node\x12\x16.learn_raft.RemoveNode\x1a\x1e.learn_raft.RemoveNodeResponse"\x00\x12\x41\n\tget_nodes\x12\x14.learn_raft.GetNodes\x1a\x1c.learn_raft.GetNodesResponse"\x00\x12O\n\rupdate_leader\x12\x19.learn_raft.AppendEntries\x1a!.learn_raft.AppendEntriesResponse"\x00\x62\x06proto3'
)


_GETNODES = DESCRIPTOR.message_types_by_name["GetNodes"]
_GETNODESRESPONSE = DESCRIPTOR.message_types_by_name["GetNodesResponse"]
_HEARTBEAT = DESCRIPTOR.message_types_by_name["HeartBeat"]
_HEARTBEATRESPONSE = DESCRIPTOR.message_types_by_name["HeartBeatResponse"]
GetNodes = _reflection.GeneratedProtocolMessageType(
    "GetNodes",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETNODES,
        "__module__": "cluster_manager_pb2"
        # @@protoc_insertion_point(class_scope:learn_raft.GetNodes)
    },
)
_sym_db.RegisterMessage(GetNodes)

GetNodesResponse = _reflection.GeneratedProtocolMessageType(
    "GetNodesResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETNODESRESPONSE,
        "__module__": "cluster_manager_pb2"
        # @@protoc_insertion_point(class_scope:learn_raft.GetNodesResponse)
    },
)
_sym_db.RegisterMessage(GetNodesResponse)

HeartBeat = _reflection.GeneratedProtocolMessageType(
    "HeartBeat",
    (_message.Message,),
    {
        "DESCRIPTOR": _HEARTBEAT,
        "__module__": "cluster_manager_pb2"
        # @@protoc_insertion_point(class_scope:learn_raft.HeartBeat)
    },
)
_sym_db.RegisterMessage(HeartBeat)

HeartBeatResponse = _reflection.GeneratedProtocolMessageType(
    "HeartBeatResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _HEARTBEATRESPONSE,
        "__module__": "cluster_manager_pb2"
        # @@protoc_insertion_point(class_scope:learn_raft.HeartBeatResponse)
    },
)
_sym_db.RegisterMessage(HeartBeatResponse)

_CLUSTERMANAGER = DESCRIPTOR.services_by_name["ClusterManager"]
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _GETNODES._serialized_start = 49
    _GETNODES._serialized_end = 59
    _GETNODESRESPONSE._serialized_start = 61
    _GETNODESRESPONSE._serialized_end = 135
    _HEARTBEAT._serialized_start = 137
    _HEARTBEAT._serialized_end = 148
    _HEARTBEATRESPONSE._serialized_start = 150
    _HEARTBEATRESPONSE._serialized_end = 169
    _CLUSTERMANAGER._serialized_start = 172
    _CLUSTERMANAGER._serialized_end = 473
# @@protoc_insertion_point(module_scope)
