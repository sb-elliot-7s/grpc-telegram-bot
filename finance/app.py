import asyncio

import grpc

import finance_pb2 as pb2
import finance_pb2_grpc as pb2_grpc
from protocols.finance_protocol import FinanceProtocol, NewsTickerProtocol
from service import FinanceService, NewsService, CacheFinanceService


class FinanceServicer(pb2_grpc.FinanceServicer):
    def __init__(self, finance_service: FinanceProtocol, news_service: NewsTickerProtocol):
        self.__news_service = news_service
        self.__finance_service = finance_service

    @staticmethod
    async def __retrieve_ticker(request: pb2.TickerRequest, context: grpc.aio.ServicerContext):
        ticker: str = request.ticker
        if ticker == '' or ticker is None:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'You must pass the name of the ticker')
        return ticker

    @staticmethod
    async def abort_invalid_argument(context: grpc.aio.ServicerContext):
        await context.abort(
            code=grpc.StatusCode.INVALID_ARGUMENT,
            details='You must pass a valid ticker name'
        )

    async def GetFinanceResponse(self, request: pb2.TickerRequest, context: grpc.aio.ServicerContext):
        ticker: str = await self.__retrieve_ticker(request=request, context=context)
        ticker_data: dict | None = await self.__finance_service.retrieve_ticker_data(ticker=ticker)
        if ticker_data is None:
            await self.abort_invalid_argument(context=context)
        return pb2.TickerResponse(**ticker_data)

    async def GetNewsResponse(self, request: pb2.TickerRequest, context: grpc.aio.ServicerContext):
        ticker: str = await self.__retrieve_ticker(request=request, context=context)
        news: list[dict] | None = await self.__news_service.retrieve_news(ticker=ticker)
        if news is None:
            await self.abort_invalid_argument(context=context)
        return pb2.NewsResponse(news=news)


async def run_server():
    server = grpc.aio.server()
    pb2_grpc.add_FinanceServicer_to_server(
        FinanceServicer(
            finance_service=CacheFinanceService(service=FinanceService()),
            news_service=NewsService()
        ),
        server
    )
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    print('start....')
    asyncio.run(run_server())
