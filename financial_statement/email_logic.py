from dataclasses import dataclass
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import aiosmtplib

from configs import get_configs
from protocols.email_service_protocol import EmailServiceProtocol


@dataclass
class EmailService(EmailServiceProtocol):
    pdf: bytes
    filename: str
    to_user: str
    from_user: str = get_configs().from_user
    email_host: str = get_configs().email_host
    email_port: int = get_configs().email_port
    email_password: str = get_configs().email_password

    async def _build_pdf_file(self, msg: MIMEMultipart):
        msg['Subject'] = self.filename
        attach = MIMEApplication(self.pdf, _subtype="pdf", name=self.filename)
        msg.attach(attach)

    async def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.from_user
        msg['To'] = self.to_user
        await self._build_pdf_file(msg=msg)
        await aiosmtplib.send(
            message=msg,
            hostname=self.email_host,
            port=self.email_port,
            username=self.from_user,
            password=self.email_password,
            start_tls=True
        )
