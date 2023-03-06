from enum import Enum

import aiogram.utils.markdown as fmt


class Constants(str, Enum):
    START_TEXT = 'Hello {username}, write /help for more information'
    
    HELP_TEXT = fmt.text(
        fmt.text(
            fmt.bold('Write command'),
            fmt.text('/news and any ticker name to watch news \\(ex\\. /news aapl\\)')
        ),
        fmt.text(
            fmt.bold('Write ticker name'),
            fmt.text('for financial information \\(ex\\. intc or qcom\\)')
        ),
        sep='\n\n'
    )


class Commands(str, Enum):
    start = 'start'
    help = 'help'
    news = 'news'
