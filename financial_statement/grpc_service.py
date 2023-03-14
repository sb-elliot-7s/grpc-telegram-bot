from dataclasses import dataclass

import grpc

import financial_statement_pb2 as rpb2
from protocols.grpc_service_protocol import GRPCServiceProtocol


@dataclass
class GRPCReceiver(GRPCServiceProtocol):
    context: grpc.aio.ServicerContext
    pdf: bytes
    symbol: str
    year: str

    async def response(self):
        return rpb2.FinancialStatementResponse(
            symbol=self.symbol,
            pdf=self.pdf,
            year=self.year
        )
