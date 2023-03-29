from dataclasses import dataclass

from constants import TypePDFResponse
from protocols.file_service_protocol import FileProtocol
from protocols.pdf_generator_protocol import PDFGeneratorProtocol


@dataclass
class FileService:
    file_service: FileProtocol
    pdf_resp: str
    pdf_service: PDFGeneratorProtocol
    filename: str

    async def execute(self) -> bytes | str:
        return self.pdf_service.url if self.pdf_resp == TypePDFResponse.PDF_URL.value else await self._download_pdf()

    async def _download_pdf(self) -> bytes | str:
        return await self._load_pdf_from_store() if await self._is_file_exist() else await self._generate_pdf()

    async def _is_file_exist(self) -> bool:
        return await self.file_service.is_file_exist(filename=self.filename)

    async def _load_pdf_from_store(self) -> bytes | str:
        return await self.file_service.download_pdf(filename=self.filename)

    async def _generate_pdf(self) -> bytes:
        return await self.pdf_service.execute()
