import asyncio
import re

import aiohttp
from aiogram import types, Bot

from configs import get_configs
from schemas import FinancialStatementRequestSchema, TypePDFResponse


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
            if response.status == 200:
                return await response.json()


def __get_extra_argument(extra_argument: list):
    return TypePDFResponse.PDF_BYTES \
        if len(extra_argument) == 1 and extra_argument[0] == 'doc' \
        else TypePDFResponse.PDF_URL


async def __warning_correct_argument(message: types.Message):
    return await message.answer(
        text='You must pass correct email or if you register email write "email" or if you want '
             'to get pdf file write "doc"')


def is_email_valid(email: str) -> bool:
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return False if not re.fullmatch(regex, email) else True


async def __matching_arguments(symbol: str, second_arg: str, saved_email: str, message: types.Message, pdf_type):
    match second_arg:
        case str() as em if em != 'doc' and saved_email is None:
            if not is_email_valid(email=em):
                return await message.answer(text='Not valid email')
            return FinancialStatementRequestSchema(symbol=symbol, email=em, pdf_response=pdf_type)
        case 'email':
            return FinancialStatementRequestSchema(symbol=symbol, email=saved_email, pdf_response=pdf_type)
        case 'doc':
            return FinancialStatementRequestSchema(symbol=symbol, pdf_response=TypePDFResponse.PDF_BYTES)
        case _:
            return await __warning_correct_argument(message=message)


async def get_report_schema(message: types.Message):
    options = {'path': f'/users/{message.from_user.id}'}
    response = await request(**options)
    returned_email = response.get('email')
    match message.get_args().split():
        case [symbol]:
            return FinancialStatementRequestSchema(symbol=symbol)
        case [symbol, second_arg, *extra_argument]:
            pdf_response = __get_extra_argument(extra_argument=extra_argument)
            return await __matching_arguments(
                symbol=symbol,
                message=message,
                second_arg=second_arg,
                saved_email=returned_email,
                pdf_type=pdf_response
            )
        case _:
            return await message.answer(text='You must pass ticker or [ticker and email]')


async def handle_email_command(bot: Bot, message: types.Message, text: str, sleep: int = 2):
    msg = await message.answer(text=text)
    await asyncio.sleep(sleep)
    await bot.delete_message(chat_id=message.from_user.id, message_id=msg.message_id)
