import base64
import gzip
import logging
from dataclasses import dataclass, field

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.remote_connection import LOGGER

from local_pdf_download import PDFDownload

LOGGER.setLevel(logging.WARNING)


@dataclass
class PdfGenerator:
    file_service: PDFDownload = PDFDownload(folder='reports')
    driver: WebDriver = field(init=False)

    def __post_init__(self):
        webdriver_options = ChromeOptions()
        webdriver_options.add_argument('--headless')
        webdriver_options.page_load_strategy = 'normal'
        webdriver_options.add_argument('--no-sandbox')
        webdriver_options.add_argument('--disable-gpu')
        webdriver_options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/111.0.0.0 Safari/537.36')
        webdriver_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(
            service=ChromeService(executable_path='/usr/local/bin/chromedriver'),
            options=webdriver_options
        )

    async def _generate_pdf(self, url: str):
        self.driver.get(url=url)
        print_options = {
            'paperWidth': 6.97,
            'paperHeight': 11.0,
        }
        result = self.driver.execute_cdp_cmd("Page.printToPDF", print_options)['data']
        return base64.b64decode(result)

    async def main(self, url: str, symbol: str, year: str = '2022') -> bytes:
        pdf = await self._generate_pdf(url=url)
        await self.file_service.save_pdf(symbol=symbol, year=year, pdf=pdf)
        return gzip.compress(pdf)
