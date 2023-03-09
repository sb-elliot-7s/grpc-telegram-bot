from dataclasses import dataclass

import finance_pb2 as pb2
from news_view import NewsView
from protocols.formatter_protocols import IFormat
from ticker_data_view import TickerView
from utils import telegram_text_format
from widgets import NewLine, BoldTitle, Link, Title, Publisher, Date, RelatedTickers


@dataclass
class Formatter:
    formatter: IFormat

    def format(self):
        return self.formatter.format()


def get_news_data(news: list[dict]):
    return ''.join(
        [
            Formatter(
                formatter=NewsView(
                    data=n,
                    new_line=NewLine(),
                    link=Link(),
                    title=Title(),
                    publisher=Publisher(),
                    date_=Date(),
                    related_tickers=RelatedTickers()
                )
            ).format() for n in news
        ]
    )


def get_ticker_data(ticker: str, data: pb2.TickerResponse):
    url = f'https://finance.yahoo.com/quote/{ticker.upper()}'
    opt = {
        'formatter': TickerView(
            bold_title=BoldTitle(),
            new_line=NewLine(),
            data=data,
            ticker=ticker
        )
    }
    ticker = Formatter(**opt).format()
    url = telegram_text_format(text=f'\n{url}')
    return f'{ticker} {url}'


def get_tickers_data(data: list[pb2.TickerResponse]) -> str:
    return ''.join([f'{get_ticker_data(ticker=ticker.ticker, data=ticker)}\n\n' for ticker in data])
