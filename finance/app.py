import asyncio

import grpc

import finance_pb2_grpc as pb2_grpc
from configs import get_configs
from finance_service import FinanceService, CacheFinanceService
from news_service import NewsService
from servicer import FinanceServicer


def get_finance_service(debug: bool):
    return FinanceService() if debug else CacheFinanceService(service=FinanceService())


async def run_server():
    server = grpc.aio.server(compression=grpc.Compression.Gzip)
    finance_service = get_finance_service(debug=get_configs().debug)
    pb2_grpc.add_FinanceServicer_to_server(
        servicer=FinanceServicer(
            finance_service=finance_service, news_service=NewsService()
        ),
        server=server
    )
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    print('start....')
    asyncio.run(run_server())
