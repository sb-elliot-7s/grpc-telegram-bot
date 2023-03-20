import gzip
from dataclasses import dataclass

import aiofiles
from aiofiles import os

from protocols.file_service_protocol import FileProtocol


@dataclass
class PDFDownload(FileProtocol):
    folder: str = 'reports'

    async def save_pdf(self, filename: str, pdf: bytes):
        p = gzip.compress(pdf)
        async with aiofiles.open(
                file=f'{self.folder}/{filename}.pdf', mode='wb') as file:
            await file.write(p)

    async def download_pdf(self, filename: str):
        async with aiofiles.open(file=f'{self.folder}/{filename}.pdf', mode='rb') as file:
            return await file.read()

    async def delete_pdf(self, filename: str):
        await os.remove(path=f'{self.folder}/{filename}.pdf')

    async def is_file_exist(self, filename: str):
        return await os.path.exists(path=f'{self.folder}/{filename}.pdf')
