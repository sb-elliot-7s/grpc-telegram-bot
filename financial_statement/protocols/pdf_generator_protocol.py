import gzip
from abc import ABC, abstractmethod
from dataclasses import dataclass

from protocols.file_service_protocol import FileProtocol


@dataclass
class PDFGeneratorProtocol(ABC):
    url: str
    filename: str
    file_service: FileProtocol

    @abstractmethod
    async def generate_pdf(self) -> bytes: pass

    async def execute(self) -> bytes:
        pdf: bytes = await self.generate_pdf()
        await self.file_service.save_pdf(filename=self.filename, pdf=pdf)
        return gzip.compress(pdf)
