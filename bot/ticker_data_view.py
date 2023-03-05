from dataclasses import dataclass

import aiogram.utils.markdown as fmt

import finance_pb2 as pb2
from protocols.formatter_protocols import IFormat, IBoldTitle, INewLine


@dataclass
class TickerView(IFormat):
    bold_title: IBoldTitle
    new_line: INewLine
    ticker: str
    data: pb2.TickerResponse

    def format(self):
        return fmt.text(
            self.bold_title.build_bold_title(ticker=self.ticker),
            self.new_line.build_new_line() * 2,
            fmt.escape_md(self.data),
            sep=''
        )
