from dataclasses import dataclass

import grpc.aio

import finance_pb2 as pb2
import finance_pb2_grpc as pb2_grpc

TIMEOUT_NEWS = 3
TIMEOUT_FINANCE_DATA = 3


@dataclass
class BotGRPCClient:
    host: str = 'localhost'
    port: int = 50051

    @staticmethod
    async def __create_stub_and_message(ticker: str, channel):
        stub = pb2_grpc.FinanceStub(channel=channel)
        message = pb2.TickerRequest(ticker=ticker)
        return stub, message

    async def get_news(self, ticker: str) -> pb2.NewsResponse:
        async with grpc.aio.insecure_channel(f'{self.host}:{self.port}') as channel:
            stub, message = await self.__create_stub_and_message(ticker=ticker, channel=channel)
            return await stub.GetNewsResponse(
                message,
                # timeout=TIMEOUT_NEWS
            )

    async def get_ticker_data(self, ticker: str) -> pb2.TickerResponse:
        async with grpc.aio.insecure_channel(f'{self.host}:{self.port}') as channel:
            stub, message = await self.__create_stub_and_message(ticker=ticker, channel=channel)
            return await stub.GetFinanceResponse(
                message,
                # timeout=TIMEOUT_FINANCE_DATA
            )
