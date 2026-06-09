from pydantic import BaseModel


class InvoiceModel(BaseModel):

    invoice_id: str

    customer_id: str

    invoice_amount: float

    due_date: str

    status: str

    days_overdue: int

    amount_left: float

    amount_left_since_30_days: float

    amount_left_since_90_days: float

    amount_left_since_180_days: float