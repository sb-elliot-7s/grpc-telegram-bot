from datetime import datetime

import aiogram.utils.markdown as fmt

from protocols.formatter_protocols import INewLine, IDate, ILink, ITitle, \
    IRelatedTickers, IBoldTitle, IPublisher
from utils import telegram_text_format


class NewLine(INewLine):
    @staticmethod
    def build_new_line(): return '\n'


class Publisher(IPublisher):
    @staticmethod
    def build_publisher(publisher: str):
        return fmt.escape_md(f"Publisher: {publisher}", '\n')


class Link(ILink):
    @staticmethod
    def build_link(link: str, title: str): return fmt.link(f"Title: {title}", link)


class Title(ITitle):
    @staticmethod
    def build_title(title: str): return title


class Date(IDate):
    @staticmethod
    def build_date(time_unix: float):
        return fmt.italic(f"Date: {datetime.fromtimestamp(time_unix)}", sep='')


class BoldTitle(IBoldTitle):
    @staticmethod
    def build_bold_title(ticker: str): return fmt.bold(f'{ticker.upper()}')


class RelatedTickers(IRelatedTickers):
    @staticmethod
    def __replace_string(string: str):
        return telegram_text_format(text=string)

    def build_related_tickers(self, rel_tickers: list):
        return fmt.text('Related tickers: ', ' '.join([self.__replace_string(string=t) for t in rel_tickers]))
