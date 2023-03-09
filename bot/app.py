from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode, User
from google.protobuf.json_format import MessageToDict

import finance_pb2 as pb2
from configs import get_configs
from constants import Constants, Commands
from decorators import grpc_error_decorator
from grpc_client import BotGRPCClient
from kafka_service import KafkaService
from schemas import UserSchema
from text_formatter import get_news_data, get_ticker_data, get_tickers_data

bot = Bot(token=get_configs().api_token)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=[Commands.start.value])
async def process_start_command(message: types.Message):
    telegram_user: User = message.from_user
    user = UserSchema(**telegram_user.to_python(), date_created=message.date)
    service = KafkaService(server=get_configs().kafka_broker)
    await service.produce(topic='user', value=user.to_dict)
    await message.reply(text=Constants.START_TEXT.value.format(username=telegram_user.username))


@dp.message_handler(commands=[Commands.help.value])
async def process_help_command(message: types.Message):
    await message.reply(text=Constants.HELP_TEXT.value, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message_handler(commands=[Commands.news.value])
@grpc_error_decorator
async def retrieve_news(message: types.Message):
    match message.get_args().split():
        case [ticker]:
            news_data: pb2.NewsResponse = await BotGRPCClient(host=get_configs().grpc_host).get_news(ticker=ticker)
            news: list[dict] = MessageToDict(message=news_data)['news']
            text: str = get_news_data(news=news)
            return await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
        case _:
            return await message.answer(text=Constants.MUST_BE_ONE_SYMBOL.value)


@dp.message_handler(commands=[Commands.tickers.value])
@grpc_error_decorator
async def retrieve_tickers_data(message: types.Message):
    tickers: str = message.get_args()
    tickers_data: pb2.TickersResponse = await BotGRPCClient(host=get_configs().grpc_host) \
        .get_tickers_data(tickers=tickers)
    text = get_tickers_data(data=tickers_data.tickerResponse)
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


@dp.message_handler()
@grpc_error_decorator
async def retrieve_finance_data(message: types.Message):
    ticker = message.text
    ticker_data: pb2.TickerResponse = await BotGRPCClient(host=get_configs().grpc_host) \
        .get_ticker_data(ticker=ticker)
    text: str = get_ticker_data(ticker=message.text, data=ticker_data)
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
