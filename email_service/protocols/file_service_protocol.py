from abc import ABC, abstractmethod


class FSProtocol(ABC):
    @abstractmethod
    async def download_pdf_file(self, filename: str): pass
