from abc import ABC, abstractmethod


class FileProtocol(ABC):
    @abstractmethod
    async def save_pdf(self, filename: str, pdf: bytes):
        pass

    @abstractmethod
    async def download_pdf(self, filename: str):
        pass

    @abstractmethod
    async def delete_pdf(self, filename: str):
        pass

    @abstractmethod
    async def is_file_exist(self, filename: str):
        pass
