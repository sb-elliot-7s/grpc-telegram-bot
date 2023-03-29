import asyncio
import base64
import logging
from dataclasses import dataclass, field

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.remote_connection import LOGGER

from protocols.pdf_generator_protocol import PDFGeneratorProtocol
from schemas import PrintOptionsSchema

LOGGER.setLevel(logging.WARNING)


@dataclass
class PdfGenerator(PDFGeneratorProtocol):
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

    async def generate_pdf(self) -> bytes:
        self.driver.get(url=self.url)
        print_options_schema = PrintOptionsSchema(paperWidth=6.97, paperHeight=11.0)
        result = await asyncio.to_thread(
            self.driver.execute_cdp_cmd, 'Page.printToPDF', print_options_schema.dict()
        )
        return base64.b64decode(result['data'])
