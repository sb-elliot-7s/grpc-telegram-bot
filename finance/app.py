import asyncio

import grpc

import finance_pb2_grpc as pb2_grpc
from cache_finance_service import CacheFinanceService
from configs import get_configs
from finance_service_from_api import APIFinanceService
from news_service import NewsService
from servicer import FinanceServicer


def get_api_service(debug: bool):
    return APIFinanceService() if debug else CacheFinanceService(service=APIFinanceService())


async def run_server():
    server = grpc.aio.server(compression=grpc.Compression.Gzip)
    finance_service = get_api_service(debug=get_configs().debug)
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
