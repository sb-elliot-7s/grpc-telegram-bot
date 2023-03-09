from pydantic import BaseModel, Field


class TickerSchema(BaseModel):
    ticker: str
    currency: str
    day_high: float = Field(alias='dayHigh')
    day_low: float = Field(alias='dayLow')
    fifty_day_average: float = Field(alias='fiftyDayAverage')
    last_price: float = Field(alias='lastPrice')
    last_volume: float = Field(alias='lastVolume')
    market_cap: float = Field(alias='marketCap')
    open_: float = Field(alias='open')
    previous_close: float = Field(alias='previousClose')
    quote_type: str = Field(alias='quoteType')
    shares: int
    timezone: str
    year_change: float = Field(alias='yearChange')
    year_high: float = Field(alias='yearHigh')
    year_low: float = Field(alias='yearLow')


class NewsSchema(BaseModel):
    title: str
    publisher: str
    link: str
    provider_publish_time: int = Field(alias='providerPublishTime')
    type_: str = Field(alias='type')
    related_tickers: list[str] = Field(alias='relatedTickers')
