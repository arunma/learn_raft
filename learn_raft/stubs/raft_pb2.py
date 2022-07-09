# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: raft.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\x12\nlearn_raft\"\xad\x01\n\x0bRequestVote\x12\x16\n\tserver_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x11\n\x04term\x18\x02 \x01(\x04H\x01\x88\x01\x01\x12\x1a\n\rlast_log_term\x18\x03 \x01(\x04H\x02\x88\x01\x01\x12\x1b\n\x0elast_log_index\x18\x04 \x01(\x04H\x03\x88\x01\x01\x42\x0c\n\n_server_idB\x07\n\x05_termB\x10\n\x0e_last_log_termB\x11\n\x0f_last_log_index\"]\n\x13RequestVoteResponse\x12\x11\n\x04term\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x19\n\x0cvote_granted\x18\x02 \x01(\x08H\x01\x88\x01\x01\x42\x07\n\x05_termB\x0f\n\r_vote_granted\"\x90\x02\n\rAppendEntries\x12\x11\n\x04term\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x16\n\tleader_id\x18\x02 \x01(\rH\x01\x88\x01\x01\x12\x1a\n\rprev_log_term\x18\x03 \x01(\x04H\x02\x88\x01\x01\x12\x1b\n\x0eprev_log_index\x18\x04 \x01(\x04H\x03\x88\x01\x01\x12 \n\x13leader_commit_index\x18\x05 \x01(\x04H\x04\x88\x01\x01\x12%\n\x07\x65ntries\x18\x06 \x03(\x0b\x32\x14.learn_raft.LogEntryB\x07\n\x05_termB\x0c\n\n_leader_idB\x10\n\x0e_prev_log_termB\x11\n\x0f_prev_log_indexB\x16\n\x14_leader_commit_index\"\x82\x01\n\x08LogEntry\x12\x11\n\x04type\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x11\n\x04term\x18\x02 \x01(\x04H\x01\x88\x01\x01\x12\x12\n\x05index\x18\x03 \x01(\x04H\x02\x88\x01\x01\x12\x14\n\x07\x63ommand\x18\x04 \x01(\x0cH\x03\x88\x01\x01\x42\x07\n\x05_typeB\x07\n\x05_termB\x08\n\x06_indexB\n\n\x08_command\"\x9b\x01\n\x15\x41ppendEntriesResponse\x12+\n\x06result\x18\x01 \x01(\x0e\x32\x16.learn_raft.ResultCodeH\x00\x88\x01\x01\x12\x11\n\x04term\x18\x02 \x01(\x04H\x01\x88\x01\x01\x12\x1b\n\x0elast_log_index\x18\x03 \x01(\x04H\x02\x88\x01\x01\x42\t\n\x07_resultB\x07\n\x05_termB\x11\n\x0f_last_log_index*4\n\nResultCode\x12\x12\n\x0eRESULT_SUCCESS\x10\x00\x12\x12\n\x0eRESULT_FAILURE\x10\x01\x62\x06proto3')

_RESULTCODE = DESCRIPTOR.enum_types_by_name['ResultCode']
ResultCode = enum_type_wrapper.EnumTypeWrapper(_RESULTCODE)
RESULT_SUCCESS = 0
RESULT_FAILURE = 1


_REQUESTVOTE = DESCRIPTOR.message_types_by_name['RequestVote']
_REQUESTVOTERESPONSE = DESCRIPTOR.message_types_by_name['RequestVoteResponse']
_APPENDENTRIES = DESCRIPTOR.message_types_by_name['AppendEntries']
_LOGENTRY = DESCRIPTOR.message_types_by_name['LogEntry']
_APPENDENTRIESRESPONSE = DESCRIPTOR.message_types_by_name['AppendEntriesResponse']
RequestVote = _reflection.GeneratedProtocolMessageType('RequestVote', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTVOTE,
  '__module__' : 'raft_pb2'
  # @@protoc_insertion_point(class_scope:learn_raft.RequestVote)
  })
_sym_db.RegisterMessage(RequestVote)

RequestVoteResponse = _reflection.GeneratedProtocolMessageType('RequestVoteResponse', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTVOTERESPONSE,
  '__module__' : 'raft_pb2'
  # @@protoc_insertion_point(class_scope:learn_raft.RequestVoteResponse)
  })
_sym_db.RegisterMessage(RequestVoteResponse)

AppendEntries = _reflection.GeneratedProtocolMessageType('AppendEntries', (_message.Message,), {
  'DESCRIPTOR' : _APPENDENTRIES,
  '__module__' : 'raft_pb2'
  # @@protoc_insertion_point(class_scope:learn_raft.AppendEntries)
  })
_sym_db.RegisterMessage(AppendEntries)

LogEntry = _reflection.GeneratedProtocolMessageType('LogEntry', (_message.Message,), {
  'DESCRIPTOR' : _LOGENTRY,
  '__module__' : 'raft_pb2'
  # @@protoc_insertion_point(class_scope:learn_raft.LogEntry)
  })
_sym_db.RegisterMessage(LogEntry)

AppendEntriesResponse = _reflection.GeneratedProtocolMessageType('AppendEntriesResponse', (_message.Message,), {
  'DESCRIPTOR' : _APPENDENTRIESRESPONSE,
  '__module__' : 'raft_pb2'
  # @@protoc_insertion_point(class_scope:learn_raft.AppendEntriesResponse)
  })
_sym_db.RegisterMessage(AppendEntriesResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RESULTCODE._serialized_start=863
  _RESULTCODE._serialized_end=915
  _REQUESTVOTE._serialized_start=27
  _REQUESTVOTE._serialized_end=200
  _REQUESTVOTERESPONSE._serialized_start=202
  _REQUESTVOTERESPONSE._serialized_end=295
  _APPENDENTRIES._serialized_start=298
  _APPENDENTRIES._serialized_end=570
  _LOGENTRY._serialized_start=573
  _LOGENTRY._serialized_end=703
  _APPENDENTRIESRESPONSE._serialized_start=706
  _APPENDENTRIESRESPONSE._serialized_end=861
# @@protoc_insertion_point(module_scope)
