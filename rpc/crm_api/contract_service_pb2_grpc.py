# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import contract_service_pb2 as crm__api_dot_contract__service__pb2


class ContractServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateContractApproval = channel.unary_unary(
                '/pb_crm_api.ContractService/CreateContractApproval',
                request_serializer=crm__api_dot_contract__service__pb2.CreateContractApprovalReq.SerializeToString,
                response_deserializer=crm__api_dot_contract__service__pb2.CreateContractApprovalRsp.FromString,
                )
        self.RetrieveContractCustomer = channel.unary_unary(
                '/pb_crm_api.ContractService/RetrieveContractCustomer',
                request_serializer=crm__api_dot_contract__service__pb2.FindContractCustomerReq.SerializeToString,
                response_deserializer=crm__api_dot_contract__service__pb2.FindContractCustomerRsp.FromString,
                )
        self.BatchRetrieveContractCustomer = channel.unary_unary(
                '/pb_crm_api.ContractService/BatchRetrieveContractCustomer',
                request_serializer=crm__api_dot_contract__service__pb2.BatchFindContractCustomerReq.SerializeToString,
                response_deserializer=crm__api_dot_contract__service__pb2.BatchFindContractCustomerRsp.FromString,
                )


class ContractServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateContractApproval(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetrieveContractCustomer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchRetrieveContractCustomer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ContractServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateContractApproval': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateContractApproval,
                    request_deserializer=crm__api_dot_contract__service__pb2.CreateContractApprovalReq.FromString,
                    response_serializer=crm__api_dot_contract__service__pb2.CreateContractApprovalRsp.SerializeToString,
            ),
            'RetrieveContractCustomer': grpc.unary_unary_rpc_method_handler(
                    servicer.RetrieveContractCustomer,
                    request_deserializer=crm__api_dot_contract__service__pb2.FindContractCustomerReq.FromString,
                    response_serializer=crm__api_dot_contract__service__pb2.FindContractCustomerRsp.SerializeToString,
            ),
            'BatchRetrieveContractCustomer': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchRetrieveContractCustomer,
                    request_deserializer=crm__api_dot_contract__service__pb2.BatchFindContractCustomerReq.FromString,
                    response_serializer=crm__api_dot_contract__service__pb2.BatchFindContractCustomerRsp.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'pb_crm_api.ContractService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ContractService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateContractApproval(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb_crm_api.ContractService/CreateContractApproval',
            crm__api_dot_contract__service__pb2.CreateContractApprovalReq.SerializeToString,
            crm__api_dot_contract__service__pb2.CreateContractApprovalRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RetrieveContractCustomer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb_crm_api.ContractService/RetrieveContractCustomer',
            crm__api_dot_contract__service__pb2.FindContractCustomerReq.SerializeToString,
            crm__api_dot_contract__service__pb2.FindContractCustomerRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchRetrieveContractCustomer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/pb_crm_api.ContractService/BatchRetrieveContractCustomer',
            crm__api_dot_contract__service__pb2.BatchFindContractCustomerReq.SerializeToString,
            crm__api_dot_contract__service__pb2.BatchFindContractCustomerRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
