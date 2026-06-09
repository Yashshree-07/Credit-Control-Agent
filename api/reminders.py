import pandas as pd

from fastapi import APIRouter

from app.services.invoice_service import (
    InvoiceService
)

from app.services.reminder_service import (
    ReminderService
)

router = APIRouter()

invoice_service = InvoiceService(
    "app/data/invoices.xlsx"
)

reminder_service = ReminderService()


@router.get("/reminders/generate")
def generate_reminders():

    invoices = (
        invoice_service.process_invoices()
    )

    reminders = []

    for _, row in invoices.iterrows():

        if row["days_overdue"] > 0:

            reminder_type = (
                reminder_service
                .determine_reminder_type(
                    row["days_overdue"]
                )
            )

            message = (
                reminder_service
                .create_reminder_message(
                    company_name=row[
                        "customer_id"
                    ],
                    invoice_id=row[
                        "invoice_id"
                    ],
                    amount=row[
                        "amount_left"
                    ],
                    days_overdue=row[
                        "days_overdue"
                    ]
                )
            )

            reminders.append({

                "invoice_id":
                    row["invoice_id"],

                "reminder_type":
                    reminder_type,

                "message":
                    message
            })

    return reminders