# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: financial_statement.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x66inancial_statement.proto\":\n\x19\x46inancialStatementRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\"G\n\x1a\x46inancialStatementResponse\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x0b\n\x03pdf\x18\x02 \x01(\x0c\x12\x0c\n\x04year\x18\x03 \x01(\t2h\n\x12\x46inancialStatement\x12R\n\x15GetFinancialStatement\x12\x1a.FinancialStatementRequest\x1a\x1b.FinancialStatementResponse\"\x00\x62\x06proto3')



_FINANCIALSTATEMENTREQUEST = DESCRIPTOR.message_types_by_name['FinancialStatementRequest']
_FINANCIALSTATEMENTRESPONSE = DESCRIPTOR.message_types_by_name['FinancialStatementResponse']
FinancialStatementRequest = _reflection.GeneratedProtocolMessageType('FinancialStatementRequest', (_message.Message,), {
  'DESCRIPTOR' : _FINANCIALSTATEMENTREQUEST,
  '__module__' : 'financial_statement_pb2'
  # @@protoc_insertion_point(class_scope:FinancialStatementRequest)
  })
_sym_db.RegisterMessage(FinancialStatementRequest)

FinancialStatementResponse = _reflection.GeneratedProtocolMessageType('FinancialStatementResponse', (_message.Message,), {
  'DESCRIPTOR' : _FINANCIALSTATEMENTRESPONSE,
  '__module__' : 'financial_statement_pb2'
  # @@protoc_insertion_point(class_scope:FinancialStatementResponse)
  })
_sym_db.RegisterMessage(FinancialStatementResponse)

_FINANCIALSTATEMENT = DESCRIPTOR.services_by_name['FinancialStatement']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _FINANCIALSTATEMENTREQUEST._serialized_start=29
  _FINANCIALSTATEMENTREQUEST._serialized_end=87
  _FINANCIALSTATEMENTRESPONSE._serialized_start=89
  _FINANCIALSTATEMENTRESPONSE._serialized_end=160
  _FINANCIALSTATEMENT._serialized_start=162
  _FINANCIALSTATEMENT._serialized_end=266
# @@protoc_insertion_point(module_scope)
