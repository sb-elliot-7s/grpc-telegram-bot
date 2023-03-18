import gzip
from dataclasses import dataclass

import grpc

import financial_statement_pb2 as rpb2
import financial_statement_pb2_grpc as rpb2_grpc
from protocols.financial_statements_service_protocol import FinancialStatementServiceProtocol
from schemas import FinancialStatementResponseSchema, FinancialStatementRequestSchema


@dataclass
class GRPCReportsClient(FinancialStatementServiceProtocol):
    host: str = 'localhost'
    port: int = 50052

    async def get_financial_statement(self, schema: FinancialStatementRequestSchema):
        channel_opt = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                       ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        async with grpc.aio.insecure_channel(f'{self.host}:{self.port}', options=channel_opt) as channel:
            stub = rpb2_grpc.FinancialStatementStub(channel=channel)
            message = rpb2.FinancialStatementRequest(**schema.dict())
            document = await stub.GetFinancialStatement(message)
            return FinancialStatementResponseSchema(
                symbol=document.symbol,
                pdf=gzip.decompress(document.pdf) if document.pdf else None,
                year=document.year,
                pdf_url=document.pdf_url
            )
