import gzip
from dataclasses import dataclass

import aiofiles


@dataclass
class PDFDownload:
    folder: str

    async def save_pdf(self, symbol: str, year: str, pdf: bytes):
        p = gzip.compress(pdf)
        async with aiofiles.open(
                file=f'{self.folder}/{symbol}:{year}.pdf', mode='wb') as file:
            await file.write(p)

    async def load_pdf(self, filename: str):
        async with aiofiles.open(file=f'{self.folder}/{filename}.pdf', mode='rb') as file:
            return await file.read()
