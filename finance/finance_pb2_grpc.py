# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import finance_pb2 as finance__pb2


class FinanceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFinanceResponse = channel.unary_unary(
                '/Finance/GetFinanceResponse',
                request_serializer=finance__pb2.TickerRequest.SerializeToString,
                response_deserializer=finance__pb2.TickerResponse.FromString,
                )
        self.GetNewsResponse = channel.unary_unary(
                '/Finance/GetNewsResponse',
                request_serializer=finance__pb2.TickerRequest.SerializeToString,
                response_deserializer=finance__pb2.NewsResponse.FromString,
                )
        self.GetTickersResponse = channel.unary_unary(
                '/Finance/GetTickersResponse',
                request_serializer=finance__pb2.TickerRequest.SerializeToString,
                response_deserializer=finance__pb2.TickersResponse.FromString,
                )


class FinanceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetFinanceResponse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNewsResponse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTickersResponse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FinanceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFinanceResponse': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFinanceResponse,
                    request_deserializer=finance__pb2.TickerRequest.FromString,
                    response_serializer=finance__pb2.TickerResponse.SerializeToString,
            ),
            'GetNewsResponse': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNewsResponse,
                    request_deserializer=finance__pb2.TickerRequest.FromString,
                    response_serializer=finance__pb2.NewsResponse.SerializeToString,
            ),
            'GetTickersResponse': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTickersResponse,
                    request_deserializer=finance__pb2.TickerRequest.FromString,
                    response_serializer=finance__pb2.TickersResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Finance', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Finance(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetFinanceResponse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Finance/GetFinanceResponse',
            finance__pb2.TickerRequest.SerializeToString,
            finance__pb2.TickerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNewsResponse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Finance/GetNewsResponse',
            finance__pb2.TickerRequest.SerializeToString,
            finance__pb2.NewsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTickersResponse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Finance/GetTickersResponse',
            finance__pb2.TickerRequest.SerializeToString,
            finance__pb2.TickersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
