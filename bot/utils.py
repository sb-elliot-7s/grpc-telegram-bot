import asyncio

import aiohttp
from aiogram import types, Bot

from configs import get_configs
from schemas import FinancialStatementRequestSchema


def telegram_text_format(text: str):
    return text. \
        replace('_', '\\_'). \
        replace('*', '\\*'). \
        replace('[', '\\['). \
        replace(']', '\\]'). \
        replace('(', '\\('). \
        replace(')', '\\)'). \
        replace('~', '\\~'). \
        replace('`', '\\`'). \
        replace('>', '\\>'). \
        replace('#', '\\#'). \
        replace('+', '\\+'). \
        replace('-', '\\-'). \
        replace('=', '\\='). \
        replace('|', '\\|'). \
        replace('{', '\\{'). \
        replace('}', '\\}'). \
        replace('.', '\\.'). \
        replace('!', '\\!')


async def request(*, base_url: str = f'http://{get_configs().api_host}:8000', path: str, headers: dict = None) -> dict:
    async with aiohttp.ClientSession(base_url=base_url, headers=headers) as session:
        async with session.get(url=path) as response:
            return await response.json()


async def get_report_schema(message: types.Message):
    options = {'path': f'/users/{message.from_user.id}'}
    response = await request(**options)
    returned_email = response.get('email')
    match message.get_args().split():
        case [symbol]:
            report_schema = FinancialStatementRequestSchema(symbol=symbol)
        case [symbol, email] if returned_email is None:
            report_schema = FinancialStatementRequestSchema(symbol=symbol, email=email)
        case [symbol, str(arg)] if arg == 'email':
            report_schema = FinancialStatementRequestSchema(symbol=symbol, email=returned_email)
        case _:
            return await message.answer(text='You must pass ticker or [ticker and email]')
    return report_schema


async def handle_email_result(bot: Bot, message: types.Message, text: str, sleep: int = 2):
    msg = await message.answer(text=text)
    await asyncio.sleep(sleep)
    await bot.delete_message(chat_id=message.from_user.id, message_id=msg.message_id)
