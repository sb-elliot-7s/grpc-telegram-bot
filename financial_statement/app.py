import asyncio

import grpc

import financial_statement_pb2_grpc as rp2_grpc
from servicer import FinancialGRPCServicer


async def run():
    server = grpc.aio.server()
    rp2_grpc.add_FinancialStatementServicer_to_server(servicer=FinancialGRPCServicer(), server=server)
    server.add_insecure_port('[::]:50052')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    print('...start...')
    asyncio.run(run())
