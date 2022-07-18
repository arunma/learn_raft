# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import learn_raft.stubs.raft_pb2 as raft__pb2


class RaftStub(object):
    """rpc"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.request_vote = channel.unary_unary(
            "/learn_raft.Raft/request_vote",
            request_serializer=raft__pb2.RequestVote.SerializeToString,
            response_deserializer=raft__pb2.RequestVoteResponse.FromString,
        )
        self.append_entries = channel.unary_unary(
            "/learn_raft.Raft/append_entries",
            request_serializer=raft__pb2.AppendEntries.SerializeToString,
            response_deserializer=raft__pb2.AppendEntriesResponse.FromString,
        )
        self.add_node = channel.unary_unary(
            "/learn_raft.Raft/add_node",
            request_serializer=raft__pb2.AddNode.SerializeToString,
            response_deserializer=raft__pb2.AddNodeResponse.FromString,
        )
        self.remove_node = channel.unary_unary(
            "/learn_raft.Raft/remove_node",
            request_serializer=raft__pb2.RemoveNode.SerializeToString,
            response_deserializer=raft__pb2.RemoveNodeResponse.FromString,
        )
        self.get_state = channel.unary_unary(
            "/learn_raft.Raft/get_state",
            request_serializer=raft__pb2.GetState.SerializeToString,
            response_deserializer=raft__pb2.GetStateResponse.FromString,
        )


class RaftServicer(object):
    """rpc"""

    def request_vote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def append_entries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def add_node(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def remove_node(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def get_state(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_RaftServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "request_vote": grpc.unary_unary_rpc_method_handler(
            servicer.request_vote,
            request_deserializer=raft__pb2.RequestVote.FromString,
            response_serializer=raft__pb2.RequestVoteResponse.SerializeToString,
        ),
        "append_entries": grpc.unary_unary_rpc_method_handler(
            servicer.append_entries,
            request_deserializer=raft__pb2.AppendEntries.FromString,
            response_serializer=raft__pb2.AppendEntriesResponse.SerializeToString,
        ),
        "add_node": grpc.unary_unary_rpc_method_handler(
            servicer.add_node,
            request_deserializer=raft__pb2.AddNode.FromString,
            response_serializer=raft__pb2.AddNodeResponse.SerializeToString,
        ),
        "remove_node": grpc.unary_unary_rpc_method_handler(
            servicer.remove_node,
            request_deserializer=raft__pb2.RemoveNode.FromString,
            response_serializer=raft__pb2.RemoveNodeResponse.SerializeToString,
        ),
        "get_state": grpc.unary_unary_rpc_method_handler(
            servicer.get_state,
            request_deserializer=raft__pb2.GetState.FromString,
            response_serializer=raft__pb2.GetStateResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler("learn_raft.Raft", rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Raft(object):
    """rpc"""

    @staticmethod
    def request_vote(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/learn_raft.Raft/request_vote",
            raft__pb2.RequestVote.SerializeToString,
            raft__pb2.RequestVoteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def append_entries(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/learn_raft.Raft/append_entries",
            raft__pb2.AppendEntries.SerializeToString,
            raft__pb2.AppendEntriesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def add_node(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/learn_raft.Raft/add_node",
            raft__pb2.AddNode.SerializeToString,
            raft__pb2.AddNodeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def remove_node(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/learn_raft.Raft/remove_node",
            raft__pb2.RemoveNode.SerializeToString,
            raft__pb2.RemoveNodeResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def get_state(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/learn_raft.Raft/get_state",
            raft__pb2.GetState.SerializeToString,
            raft__pb2.GetStateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
