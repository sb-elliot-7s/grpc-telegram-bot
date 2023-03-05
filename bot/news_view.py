from dataclasses import dataclass

import aiogram.utils.markdown as fmt

from protocols.formatter_protocols import IFormat, INewLine, IPublisher, ITitle, ILink, IDate, IRelatedTickers


@dataclass
class NewsView(IFormat):
    data: dict
    new_line: INewLine
    publisher: IPublisher
    title: ITitle
    link: ILink
    date_: IDate
    related_tickers: IRelatedTickers

    def build_title(self):
        return self.title.build_title(title=self.data.get('title'))

    def build_link(self):
        return self.link.build_link(link=self.data.get('link'), title=self.build_title())

    def build_publisher(self):
        return self.publisher.build_publisher(publisher=self.data.get('publisher'))

    def build_date(self):
        return self.date_.build_date(time_unix=self.data.get('providerPublishTime'))

    def build_new_line(self):
        return self.new_line.build_new_line()

    def build_related_tickers(self, rel_tickers: list):
        return self.related_tickers.build_related_tickers(rel_tickers=rel_tickers)

    def format(self):
        return fmt.text(
            self.build_link(),
            self.build_new_line(),
            self.build_publisher(),
            self.build_date(),
            self.build_new_line(),
            self.build_related_tickers(self.data.get('relatedTickers', [])),
            self.build_new_line() * 2,
            sep=''
        )
