import logging

import grpc

import financial_statement_pb2 as rpb2
import financial_statement_pb2_grpc as rpb2_grpc
from api_service import APIFinancialStatementService
from command_client import CommandClient
from constants import TypeFileReturned
from email_kafka_command import EmailKafkaCommand
from email_kafka_receiver import EmailKafkaReceiver
from file_service import FileService
from grpc_command import GRPCCommand
from grpc_receiver import GRPCReceiver
from pdf_service import PdfGenerator
from protocols.command_protocols import Command
from s3_storage import S3StorageFileService
from schemas import KafkaEmailPayloadSchema, FilenameSchema
from utils import Utils

logging.basicConfig(level=logging.DEBUG, filename='b.log')


class FinancialGRPCServicer(rpb2_grpc.FinancialStatementServicer, Utils):
    CONTEXT = grpc.aio.ServicerContext
    GRPC_REQUEST = rpb2.FinancialStatementRequest

    async def GetFinancialStatement(self, request: GRPC_REQUEST, context: CONTEXT):
        report: dict = await APIFinancialStatementService().get_report(symbol=request.symbol, context=context)
        logging.debug('REPORT: %s', report)
        year: str = self.parse_year(report_dict=report)

        pdf: str | bytes = await self._get_pdf(request=request, year=year, link=report.get('finalLink'))
        command: Command = await self._get_command(context=context, req=request, pdf=pdf, year=year)
        return await CommandClient(command=command).process()

    @staticmethod
    async def _get_pdf(request: GRPC_REQUEST, year: str, link: str) -> bytes | str:
        file_service = S3StorageFileService(type_file_returned=TypeFileReturned.URL)
        filename: str = FilenameSchema(symbol=request.symbol, year=year).filename
        return await FileService(
            file_service=file_service,
            pdf_resp=request.pdf_response,
            filename=filename,
            pdf_service=PdfGenerator(file_service=file_service, filename=filename, url=link)
        ).execute()

    async def _get_command(self, context: CONTEXT, req: GRPC_REQUEST, pdf: bytes | str, year: str) -> Command:
        grpc_command = GRPCCommand(receiver=GRPCReceiver(context=context, pdf=pdf, symbol=req.symbol, year=year))
        data = KafkaEmailPayloadSchema(
            filename=FilenameSchema(symbol=req.symbol, year=year).filename,
            to_user=req.email,
            link=self.get_pdf_url_or_none(pdf=pdf)
        )
        kafka_email_command = EmailKafkaCommand(command=grpc_command, receiver=EmailKafkaReceiver(**data.dict()))
        return kafka_email_command if req.email else grpc_command
