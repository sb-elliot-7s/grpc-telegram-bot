from dataclasses import dataclass

import grpc

import financial_statement_pb2 as rpb2
from protocols.grpc_service_protocol import GRPCServiceProtocol


@dataclass
class GRPCReceiver(GRPCServiceProtocol):
    context: grpc.aio.ServicerContext
    pdf: bytes | str
    symbol: str
    year: str

    async def response(self):
        pdf_url = self.pdf if isinstance(self.pdf, str) else None
        pdf_bytes = self.pdf if isinstance(self.pdf, bytes) else None
        return rpb2.FinancialStatementResponse(symbol=self.symbol, pdf=pdf_bytes, year=self.year, pdf_url=pdf_url)
