import asyncio

import grpc

import finance_pb2 as pb2
import finance_pb2_grpc as pb2_grpc
from configs import get_configs
from finance_service import FinanceService, CacheFinanceService
from news_service import NewsService
from protocols.finance_protocol import FinanceProtocol, NewsTickerProtocol


class FinanceServicer(pb2_grpc.FinanceServicer):
    def __init__(self, finance_service: FinanceProtocol, news_service: NewsTickerProtocol):
        self.__news_service = news_service
        self.__finance_service = finance_service

    @staticmethod
    async def __abort_invalid_argument(context: grpc.aio.ServicerContext):
        options = {'code': grpc.StatusCode.INVALID_ARGUMENT, 'details': 'You must pass a valid ticker name'}
        await context.abort(**options)

    async def __retrieve_ticker(self, request: pb2.TickerRequest, context: grpc.aio.ServicerContext):
        ticker: str = request.ticker
        if ticker == '' or ticker is None:
            await self.__abort_invalid_argument(context=context)
        return ticker

    Data = dict | list[dict] | None

    async def __check_if_data_is_none(self, data: Data, context: grpc.aio.ServicerContext):
        if data is None:
            await self.__abort_invalid_argument(context=context)

    async def GetFinanceResponse(self, request: pb2.TickerRequest, context: grpc.aio.ServicerContext):
        ticker: str = await self.__retrieve_ticker(request=request, context=context)
        ticker_data: dict | None = await self.__finance_service.retrieve_ticker_data(ticker=ticker)
        await self.__check_if_data_is_none(data=ticker_data, context=context)
        return pb2.TickerResponse(**ticker_data)

    async def GetNewsResponse(self, request: pb2.TickerRequest, context: grpc.aio.ServicerContext):
        ticker: str = await self.__retrieve_ticker(request=request, context=context)
        news: list[dict] | None = await self.__news_service.retrieve_news(ticker=ticker)
        await self.__check_if_data_is_none(data=news, context=context)
        return pb2.NewsResponse(news=news)

    async def GetTickersResponse(self, request: pb2.TickerRequest, context: grpc.aio.ServicerContext):
        tickers = request.ticker.split()
        tickers_data: list[dict] = await self.__finance_service.retrieve_tickers_data(tickers=tickers)
        await self.__check_if_data_is_none(data=tickers_data, context=context)
        return pb2.TickersResponse(tickerResponse=tickers_data)


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
