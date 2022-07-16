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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x63luster_manager.proto\x12\nlearn_raft\x1a\nraft.proto\"\t\n\x07GetNode\"6\n\x0fGetNodeResponse\x12#\n\x07servers\x18\x01 \x03(\x0b\x32\x12.learn_raft.Server\"\x0b\n\tHeartBeat\"\x13\n\x11HeartBeatResponse2\xda\x01\n\x0e\x43lusterManager\x12>\n\x08\x61\x64\x64_node\x12\x13.learn_raft.AddNode\x1a\x1b.learn_raft.AddNodeResponse\"\x00\x12G\n\x0bremove_node\x12\x16.learn_raft.RemoveNode\x1a\x1e.learn_raft.RemoveNodeResponse\"\x00\x12?\n\tget_nodes\x12\x13.learn_raft.GetNode\x1a\x1b.learn_raft.GetNodeResponse\"\x00\x62\x06proto3')



_GETNODE = DESCRIPTOR.message_types_by_name['GetNode']
_GETNODERESPONSE = DESCRIPTOR.message_types_by_name['GetNodeResponse']
_HEARTBEAT = DESCRIPTOR.message_types_by_name['HeartBeat']
_HEARTBEATRESPONSE = DESCRIPTOR.message_types_by_name['HeartBeatResponse']
GetNode = _reflection.GeneratedProtocolMessageType('GetNode', (_message.Message,), {
  'DESCRIPTOR' : _GETNODE,
  '__module__' : 'cluster_manager_pb2'
  # @@protoc_insertion_point(class_scope:learn_raft.GetNode)
  })
_sym_db.RegisterMessage(GetNode)

GetNodeResponse = _reflection.GeneratedProtocolMessageType('GetNodeResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETNODERESPONSE,
  '__module__' : 'cluster_manager_pb2'
  # @@protoc_insertion_point(class_scope:learn_raft.GetNodeResponse)
  })
_sym_db.RegisterMessage(GetNodeResponse)

HeartBeat = _reflection.GeneratedProtocolMessageType('HeartBeat', (_message.Message,), {
  'DESCRIPTOR' : _HEARTBEAT,
  '__module__' : 'cluster_manager_pb2'
  # @@protoc_insertion_point(class_scope:learn_raft.HeartBeat)
  })
_sym_db.RegisterMessage(HeartBeat)

HeartBeatResponse = _reflection.GeneratedProtocolMessageType('HeartBeatResponse', (_message.Message,), {
  'DESCRIPTOR' : _HEARTBEATRESPONSE,
  '__module__' : 'cluster_manager_pb2'
  # @@protoc_insertion_point(class_scope:learn_raft.HeartBeatResponse)
  })
_sym_db.RegisterMessage(HeartBeatResponse)

_CLUSTERMANAGER = DESCRIPTOR.services_by_name['ClusterManager']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETNODE._serialized_start=49
  _GETNODE._serialized_end=58
  _GETNODERESPONSE._serialized_start=60
  _GETNODERESPONSE._serialized_end=114
  _HEARTBEAT._serialized_start=116
  _HEARTBEAT._serialized_end=127
  _HEARTBEATRESPONSE._serialized_start=129
  _HEARTBEATRESPONSE._serialized_end=148
  _CLUSTERMANAGER._serialized_start=151
  _CLUSTERMANAGER._serialized_end=369
# @@protoc_insertion_point(module_scope)