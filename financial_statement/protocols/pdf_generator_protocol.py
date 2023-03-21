from abc import ABC, abstractmethod


class PDFGeneratorProtocol(ABC):
    @abstractmethod
    async def generate_pdf(self) -> bytes: pass
