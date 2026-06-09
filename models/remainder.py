from pydantic import BaseModel


class ReminderModel(BaseModel):

    invoice_id: str

    reminder_type: str

    sent_date: str