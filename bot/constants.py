from enum import Enum

import aiogram.utils.markdown as fmt


class Constants(str, Enum):
    START_TEXT = 'Hello {username}, write /help for more information'
    HELP_TEXT = fmt.text(
        fmt.text(
            fmt.bold('Write command'),
            fmt.text('/ticker \\+ symbol \\- show financial information for one stock')
        ),
        fmt.text(
            fmt.bold('Write command'),
            fmt.text('/news \\+ symbol \\- show the news for the specified symbol')
        ),
        fmt.text(
            fmt.bold('Write command'),
            fmt.text(
                '/tickers \\+ symbols show financial information for stocks example: amd qcom aapl t')
        ),
        fmt.text(
            fmt.bold('Write command'),
            fmt.text('/email \\- saving your email to db or write "rm" for deleting email from db')
        ),
        fmt.text(
            fmt.bold('Write command'),
            fmt.text(
                '/report \\+ one stock show report for last year, '
                '\\[\\["email" or your email@gmail\\.com if you not set email in /email command\\], '
                '"doc" if you want pdf file not url\\]')
        ),
        sep='\n\n'
    )
    MUST_BE_ONE_SYMBOL = 'You must pass one ticker symbol'


class Commands(str, Enum):
    START = 'start'
    HELP = 'help'
    TICKER = 'ticker'
    NEWS = 'news'
    TICKERS = 'tickers'
    EMAIL = 'email'
    REPORTS = 'report'
    ACCOUNT = 'acc'


class Topic(str, Enum):
    SAVE_EMAIL = 'save_email'
    USER = 'user'
    REMOVE_EMAIL = 'remove_email'


help_commands = {
    '/start': 'start bot',
    '/email': 'saving your email to db or write "rm" for deleting email from db',
    '/tickers': 'show financial information for stocks example: amd, qcom, aapl, t',
    '/report': '+ one stock show report for last year, '
               '[["email" or your email@gmail.com if you not set email in /email command], '
               '"doc" if you want pdf file not url]',
    '/news': 'show the news for the specified symbol',
    '/ticker': 'show financial information for one stock'
}
