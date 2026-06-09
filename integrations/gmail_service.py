import base64

from email.mime.text import MIMEText

from google.auth.transport.requests import (
    Request
)

from google.oauth2.credentials import (
    Credentials
)

from google_auth_oauthlib.flow import (
    InstalledAppFlow
)

from googleapiclient.discovery import (
    build
)

import os.path


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]


class GmailService:

    def __init__(self):

        self.service = self.authenticate()

    def authenticate(self):

        creds = None

        if os.path.exists("token.json"):

            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

        if (
            not creds
            or not creds.valid
        ):

            if (
                creds
                and creds.expired
                and creds.refresh_token
            ):

                creds.refresh(
                    Request()
                )

            else:

                flow = (
                    InstalledAppFlow
                    .from_client_secrets_file(
                        "credentials.json",
                        SCOPES
                    )
                )

                creds = (
                    flow.run_local_server(
                        port=0
                    )
                )

            with open(
                "token.json",
                "w"
            ) as token:

                token.write(
                    creds.to_json()
                )

        return build(
            "gmail",
            "v1",
            credentials=creds
        )

    def send_email(
        self,
        to_email,
        subject,
        message_text
    ):

        message = MIMEText(
            message_text
        )

        message["to"] = to_email

        message["subject"] = subject

        raw = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        message_body = {
            "raw": raw
        }

        self.service.users().messages().send(
            userId="me",
            body=message_body
        ).execute()

    def read_unread_emails(self):

        results = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                labelIds=["INBOX"],
                q="is:unread"
            )
            .execute()
        )

        messages = results.get(
            "messages",
            []
        )

        email_data = []

        for msg in messages:

            txt = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=msg["id"]
                )
                .execute()
            )

            payload = txt["payload"]

            headers = payload["headers"]

            subject = ""

            sender = ""

            for d in headers:

                if d["name"] == "Subject":

                    subject = d["value"]

                if d["name"] == "From":

                    sender = d["value"]

            body = ""

            if "parts" in payload:

                parts = payload["parts"]

                data = parts[0]["body"].get(
                    "data"
                )

                if data:

                    body = base64.urlsafe_b64decode(
                        data
                    ).decode()

            email_data.append({

                "id": msg["id"],
                "subject": subject,
                "from": sender,
                "body": body
            })

        return email_data

    