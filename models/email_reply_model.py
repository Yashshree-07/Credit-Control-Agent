from pydantic import BaseModel


class EmailReplyModel(BaseModel):

    company_name: str

    email_text: str

    detected_intent: str