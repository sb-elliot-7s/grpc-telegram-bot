from dataclasses import dataclass
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import aiosmtplib

from protocols.email_service_protocol import EmailServiceProtocol
from schemas import EmailSchema


@dataclass
class EmailService(EmailServiceProtocol):
    pdf: bytes | None
    email_schema: EmailSchema

    @staticmethod
    def __build_subject_message(msg: MIMEMultipart, text: str):
        msg['Subject'] = text

    async def __build_pdf_file_message(self, msg: MIMEMultipart):
        self.__build_subject_message(msg=msg, text=self.email_schema.filename)
        attach = MIMEApplication(self.pdf, _subtype='pdf', name=self.email_schema.filename)
        msg.attach(attach)

    async def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.email_schema.from_user
        msg['To'] = self.email_schema.to_user
        if self.pdf is not None:
            await self.__build_pdf_file_message(msg=msg)
        else:
            self.__build_subject_message(msg=msg, text=f'{self.email_schema.filename} {self.email_schema.link}')
        await aiosmtplib.send(
            message=msg,
            hostname=self.email_schema.email_host,
            port=self.email_schema.email_port,
            username=self.email_schema.from_user,
            password=self.email_schema.email_password,
            start_tls=True
        )
