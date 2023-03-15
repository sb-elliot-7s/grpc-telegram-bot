from pydantic import BaseModel, Field


class TickerSchema(BaseModel):
    symbol: str
    name: str
    price: float
    changes_percentage: float = Field(alias='changesPercentage')
    change: float
    day_low: float = Field(alias='dayLow')
    day_high: float = Field(alias='dayHigh')
    year_high: float = Field(alias='yearHigh')
    year_low: float = Field(alias='yearLow')
    market_cap: float = Field(alias='marketCap')
    price_avg50: float = Field(alias='priceAvg50')
    price_avg200: float = Field(alias='priceAvg200')
    exchange: str
    volume: float
    avg_volume: float = Field(alias='avgVolume')
    open: float
    previous_close: float = Field(alias='previousClose')
    eps: float
    pe: float
    earnings_announcement: str = Field(alias='earningsAnnouncement')
    shares_outstanding: int = Field(alias='sharesOutstanding')
    timestamp: int


# class TickerSchema(BaseModel):
#     ticker: str
#     currency: str
#     day_high: float = Field(alias='dayHigh')
#     day_low: float = Field(alias='dayLow')
#     fifty_day_average: float = Field(alias='fiftyDayAverage')
#     last_price: float = Field(alias='lastPrice')
#     last_volume: float = Field(alias='lastVolume')
#     market_cap: float = Field(alias='marketCap')
#     open_: float = Field(alias='open')
#     previous_close: float = Field(alias='previousClose')
#     quote_type: str = Field(alias='quoteType')
#     shares: int
#     timezone: str
#     year_change: float = Field(alias='yearChange')
#     year_high: float = Field(alias='yearHigh')
#     year_low: float = Field(alias='yearLow')


class NewsSchema(BaseModel):
    title: str
    publisher: str
    link: str
    provider_publish_time: int = Field(alias='providerPublishTime')
    type_: str = Field(alias='type')
    related_tickers: list[str] = Field(alias='relatedTickers')
