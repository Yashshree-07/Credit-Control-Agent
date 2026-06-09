import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from dotenv import load_dotenv

load_dotenv()


class EmailService:

    def __init__(self):

        self.sender_email = os.getenv(
            "EMAIL_SENDER"
        )

        self.password = os.getenv(
            "EMAIL_PASSWORD"
        )

        self.smtp_server = os.getenv(
            "SMTP_SERVER"
        )

        self.smtp_port = int(
            os.getenv("SMTP_PORT")
        )

    def send_email(
        self,
        recipient,
        subject,
        body
    ):

        try:

            msg = MIMEMultipart()

            msg["From"] = self.sender_email
            msg["To"] = recipient
            msg["Subject"] = subject

            msg.attach(
                MIMEText(body, "plain")
            )

            server = smtplib.SMTP(
                self.smtp_server,
                self.smtp_port
            )

            server.starttls()

            server.login(
                self.sender_email,
                self.password
            )

            server.send_message(msg)

            server.quit()

            print(
                f"Email sent to {recipient}"
            )

        except Exception as e:

            print(
                f"Email Error: {e}"
            )