from enum import Enum

import aiogram.utils.markdown as fmt


class Constants(str, Enum):
    START_TEXT = 'Hello {username}, write /help for more information'

    HELP_TEXT = fmt.text(
        fmt.text(
            fmt.bold('Write command'),
            fmt.text('/news and any ticker symbol to watch news \\(ex\\. /news aapl\\)')
        ),
        fmt.text(
            fmt.bold('Write ticker symbol'),
            fmt.text('for financial information \\(ex\\. intc or qcom\\)')
        ),
        fmt.text(
            fmt.bold('Write command'),
            fmt.text('/tickers and tickers symbols \\(ex\\. /tickers aapl intc msft amd\\)')
        ),
        fmt.text(
            fmt.bold('Write command'),
            fmt.text('/email and your email for saving email or /email and "remove" to remove your email from database')
        ),
        fmt.text(
            fmt.bold('Write command'),
            fmt.text('/report and symbol optional \\-"email" if you set email in /email command or set correct email')
        ),
        sep='\n\n'
    )
    MUST_BE_ONE_SYMBOL = 'You must pass one ticker symbol'


class Commands(str, Enum):
    start = 'start'
    help = 'help'
    news = 'news'
    tickers = 'tickers'
    email = 'email'
    reports = 'report'


class Topic(str, Enum):
    SAVE_EMAIL = 'save_email'
    USER = 'user'
    REMOVE_EMAIL = 'remove_email'
