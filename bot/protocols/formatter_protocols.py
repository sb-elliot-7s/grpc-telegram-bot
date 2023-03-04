from abc import ABC, abstractmethod


class IFormat(ABC):
    @abstractmethod
    def format(self): pass


class INewLine(ABC):
    @staticmethod
    @abstractmethod
    def build_new_line(): pass


class IPublisher(ABC):
    @staticmethod
    @abstractmethod
    def build_publisher(publisher: str): pass


class ILink(ABC):
    @staticmethod
    @abstractmethod
    def build_link(link: str, title: str): pass


class ITitle(ABC):
    @staticmethod
    @abstractmethod
    def build_title(title: str): pass


class IDate(ABC):
    @staticmethod
    @abstractmethod
    def build_date(time_unix: float): pass


class IBoldTitle(ABC):
    @staticmethod
    @abstractmethod
    def build_bold_title(ticker: str): pass


class IRelatedTickers(ABC):
    @abstractmethod
    def build_related_tickers(self, rel_tickers: list): pass
