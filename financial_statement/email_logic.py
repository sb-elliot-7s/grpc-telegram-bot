from dataclasses import dataclass
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import aiosmtplib

from protocols.email_service_protocol import EmailServiceProtocol


@dataclass
class EmailService(EmailServiceProtocol):
    pdf: bytes
    text: str
    to_user: str
    from_user: str
    email_host: str
    email_port: int
    email_password: str
    year: str

    async def send_to_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.from_user
        msg['To'] = self.to_user
        msg['Subject'] = self.text
        attach = MIMEApplication(self.pdf, _subtype="pdf", name=f'{self.text}:{self.year}')
        msg.attach(attach)
        await aiosmtplib.send(
            message=msg,
            hostname=self.email_host,
            port=self.email_port,
            username=self.from_user,
            password=self.email_password,
            start_tls=True
        )
