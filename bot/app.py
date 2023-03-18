import logging

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode, User
from aiogram.utils.markdown import link
from google.protobuf.json_format import MessageToDict

import finance_pb2 as pb2
from configs import get_configs
from constants import Constants, Commands, Topic, help_commands
from decorators import grpc_error_decorator
from grpc_finance_client import BotGRPCClient
from grpc_reports_client import GRPCReportsClient
from kafka_service import KafkaService
from schemas import FinancialStatementRequestSchema, UserSchema
from text_formatter import get_tickers_data, get_news_data, get_ticker_data
from utils import handle_email_command, get_report_schema, is_email_valid

logging.basicConfig(level=logging.DEBUG, filename='b.log')
bot = Bot(token=get_configs().api_token)
dp = Dispatcher(bot=bot)


def help_for_command(func):
    async def decorator(*args):
        message: types.Message = args[0]
        command = message.get_command()
        if message.get_command() is not None and '-h' in message.get_args():
            if (help_text := help_commands.get(command)) is not None:
                return await message.answer(text=help_text)
        return await func(*args)

    return decorator


@dp.message_handler(commands=[Commands.START.value])
@help_for_command
async def process_start_command(message: types.Message):
    telegram_user: User = message.from_user
    user = UserSchema(**telegram_user.to_python(), date_created=message.date)
    service = KafkaService(server=get_configs().kafka_broker)
    await service.produce(topic=Topic.USER.value, value=user.to_dict)
    await message.reply(text=Constants.START_TEXT.value.format(username=telegram_user.username))


@dp.message_handler(commands=[Commands.HELP.value])
async def process_help_command(message: types.Message):
    await message.reply(text=Constants.HELP_TEXT.value, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message_handler(commands=[Commands.NEWS.value])
@grpc_error_decorator
@help_for_command
async def retrieve_news(message: types.Message):
    match message.get_args().split():
        case [ticker]:
            news_data: pb2.NewsResponse = await BotGRPCClient(host=get_configs().grpc_host).get_news(ticker=ticker)
            news: list[dict] = MessageToDict(message=news_data)['news']
            text: str = get_news_data(news=news)
            return await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
        case _:
            return await message.answer(text=Constants.MUST_BE_ONE_SYMBOL.value)


@dp.message_handler(commands=[Commands.TICKERS.value])
@grpc_error_decorator
@help_for_command
async def retrieve_tickers_data(message: types.Message):
    tickers: str = message.get_args()
    tickers_data: pb2.TickersResponse = await BotGRPCClient(host=get_configs().grpc_host) \
        .get_tickers_data(tickers=tickers)
    text = get_tickers_data(data=tickers_data.tickerResponse, from_api=True)
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


@dp.message_handler(commands=[Commands.REPORTS.value])
@grpc_error_decorator
@help_for_command
async def get_financial_statement_reports(message: types.Message):
    schema: FinancialStatementRequestSchema = await get_report_schema(message=message)
    report = await GRPCReportsClient(host=get_configs().grpc_report_host).get_financial_statement(schema=schema)
    if report.pdf_url:
        url = link(title=f'Report - {report.symbol}:{report.year}', url=report.pdf_url)
        return await message.answer(text=url, parse_mode=ParseMode.MARKDOWN_V2)
    return await bot.send_document(message.from_user.id, (f'{report.symbol}:{report.year}.pdf', report.pdf))


@dp.message_handler(commands=[Commands.EMAIL.value])
@help_for_command
async def process_email(message: types.Message):
    user_id = message.from_user.id
    match message.get_args().split():
        case [str(cmd)] if cmd == 'rm':
            await KafkaService(server=get_configs().kafka_broker) \
                .produce(topic=Topic.REMOVE_EMAIL.value, value={'user_id': user_id})
            await handle_email_command(bot=bot, message=message, text='deleting email...')
        case [email]:
            if not is_email_valid(email=email):
                return await message.answer(text='Not valid email')
            await KafkaService(server=get_configs().kafka_broker) \
                .produce(topic=Topic.SAVE_EMAIL.value, value={'user_id': user_id, 'email': email})
            await handle_email_command(bot=bot, message=message, text='email saving...')
        case _:
            await message.answer(text='You must pass only one argument - correct email')


@dp.message_handler(commands=[Commands.TICKER.value])
@grpc_error_decorator
@help_for_command
async def retrieve_finance_data(message: types.Message):
    ticker = message.text.split()[-1]
    ticker_data: pb2.TickerResponse = await BotGRPCClient(host=get_configs().grpc_host) \
        .get_ticker_data(ticker=ticker)
    text: str = get_ticker_data(ticker=ticker, data=ticker_data, company_name=ticker_data.name)
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
