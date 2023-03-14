import os.path

import grpc

import financial_statement_pb2 as rpb2
import financial_statement_pb2_grpc as rp2_grpc
from api_service import FinancialStatementService
from command_client import CommandClient
from configs import get_configs
from email_command import EmailGrpcCommand
from email_logic import EmailService
from grpc_command import GRPCCommand
from grpc_service import GRPCReceiver
from local_pdf_download import PDFDownload
from pdf_service import PdfGenerator
from protocols.command_protocols import Command
from schemas import EmailDataSchema


class FinancialGRPCServicer(rp2_grpc.FinancialStatementServicer):

    async def GetFinancialStatement(self, request: rpb2.FinancialStatementRequest, context: grpc.aio.ServicerContext):
        report = await self._get_report(request=request, context=context)
        year = self.__parse_year(report_dict=report)
        pdf: bytes = await self._get_pdf(symbol=request.symbol, year=year, link=report.get('finalLink'))
        command = await self._get_command(context=context, request=request, pdf=pdf, year=year)
        return await CommandClient(command=command).process()

    async def _get_command(
            self, context: grpc.aio.ServicerContext, request: rpb2.FinancialStatementRequest, pdf: bytes,
            year: str) -> Command | str:
        grpc_command = GRPCCommand(
            receiver=GRPCReceiver(context=context, pdf=pdf, symbol=request.symbol, year=year))
        email_grpc_command = EmailGrpcCommand(command=grpc_command, email_service=EmailService(
            **self.__get_email_data(to_user=request.email, pdf=pdf, text=request.symbol, year=year)))
        return email_grpc_command if request.email else grpc_command

    @staticmethod
    def __get_email_data(text: str, pdf: bytes, to_user: str, year: str) -> dict:
        return EmailDataSchema(text=text, pdf=pdf, year=year, to_user=to_user).dict()

    @staticmethod
    def __parse_year(report_dict: dict) -> str:
        # 2022-10-27 18:01:14
        return report_dict.get('acceptedDate').split()[0].split('-')[0]

    @staticmethod
    async def __generate_pdf(symbol: str, link: str, year: str) -> bytes:
        return await PdfGenerator().main(url=link, symbol=symbol, year=year)

    @staticmethod
    async def __load_pdf(symbol: str, year: str) -> bytes:
        return await PDFDownload(folder='reports').load_pdf(filename=f'{symbol}:{year}')

    @staticmethod
    def __if_file_exist(symbol: str, year: str) -> bool:
        return os.path.exists(path=f'reports/{symbol}:{year}.pdf')

    async def _get_pdf(self, symbol: str, year: str, link: str) -> bytes:
        return await self.__load_pdf(symbol=symbol, year=year) \
            if self.__if_file_exist(symbol=symbol, year=year) \
            else await self.__generate_pdf(symbol=symbol, link=link, year=year)

    @staticmethod
    async def _get_report(request: rpb2.FinancialStatementRequest, context: grpc.aio.ServicerContext) -> dict:
        last_report = 0
        reports: list[dict] = await FinancialStatementService(base_url=get_configs().base_url) \
            .get_financial_statement_data(ticker=request.symbol)
        if not len(reports):
            await context.abort(code=grpc.StatusCode.INVALID_ARGUMENT, details='You must pass valid symbol')
        return reports[last_report]
